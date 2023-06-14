"""Text to speech"""
import io
import os
from abc import ABC, abstractmethod
from typing import Any, Optional

from google.cloud import texttospeech
from pydantic import BaseModel
from pydub import AudioSegment
from pydub.playback import play

from languageassistant.utils import country_codes


class BaseTTS(BaseModel, ABC):
    """Abstract base tts model"""

    language: str
    """TTS input language name [see Supported Languages]"""

    @abstractmethod
    def run(self, tts_input: str) -> None:
        """Converts tts input in language to audio with playback on speaker"""


class TTS(BaseTTS):
    """Multilingual TTS using the Google TTS API"""

    client: Optional[texttospeech.TextToSpeechClient] = None
    """Google TTS client"""
    voice_gender: int = texttospeech.SsmlVoiceGender.NEUTRAL
    """TTS voice gender"""
    audio_config: Optional[texttospeech.AudioConfig] = None
    """Audio config for return encoding type (MP3)"""

    class Config:
        arbitrary_types_allowed = True

    @property
    def voice(self) -> texttospeech.VoiceSelectionParams:
        """Select TTS voice from language and gender"""
        return texttospeech.VoiceSelectionParams(
            {
                "language_code": country_codes[self.language],
                "ssml_gender": self.voice_gender,
            }
        )

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if "client" not in kwargs:
            self.client = texttospeech.TextToSpeechClient(
                client_options={"api_key": os.getenv("GOOGLE_API_KEY")}
            )
        if "audio_config" not in kwargs:
            self.audio_config = texttospeech.AudioConfig(
                {"audio_encoding": texttospeech.AudioEncoding.MP3}
            )

    def _text_to_mp3(self, tts_input: str) -> bytes:
        """Convert input text to mp3 bytes"""
        synthesis_input = texttospeech.SynthesisInput({"text": tts_input})
        assert isinstance(self.client, texttospeech.TextToSpeechClient)
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=self.voice, audio_config=self.audio_config
        )
        return response.audio_content

    def run(self, tts_input: str) -> None:
        """Convert tts to audio and output to speaker"""
        mp3_bytes = self._text_to_mp3(tts_input)
        mp3_buffer = io.BytesIO(mp3_bytes)
        audio = AudioSegment.from_file(mp3_buffer, format="mp3")
        play(audio)
