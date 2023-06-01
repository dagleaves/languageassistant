"""Modified version of https://github.com/jakvb/whisper_real_time"""
import io
from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep
from typing import Any, Optional

import openai
import speech_recognition as sr

from languageassistant.utils import load_openai_api_key


class MicrophoneNotFoundError(Exception):
    """No microphone found."""


def get_transcription(temp_file: str, wav_data: io.BytesIO) -> str:
    # Write wav data to the temporary file as bytes.
    with open(temp_file, "w+b") as wf:
        wf.write(wav_data.read())

    with open(temp_file, "rb") as rf:
        result = openai.Audio.transcribe("whisper-1", rf)
    text: str = result["text"].strip()
    return text


class Transcriber:
    """Transcription model for user input."""

    def __init__(self, default_microphone: str = "list") -> None:
        load_openai_api_key()
        # Microphone Settings
        self.record_timeout: float = 2
        """How real-time the recording is."""
        self.phrase_timeout: float = 3
        """Delay before ending user monologue."""
        self.energy_threshold: int = 1000
        """Microphone energy threshold for background noise."""
        self.default_microphone: str = default_microphone
        """Default microphone name."""

        # Recording variables
        self.phrase_time: Optional[datetime] = None
        """The last time a recording was retreived from the queue."""
        self.last_sample: bytes = b""
        """Current raw audio bytes."""
        self.data_queue: Queue = Queue()
        """Thread-safe Queue for passing data from the threaded recording callback."""
        self.recorder: sr.Recognizer = sr.Recognizer()
        """SpeechRecognizer to record and detect when speech ends."""
        self.temp_file: str = NamedTemporaryFile(suffix=".wav").name
        """File for sending to OpenAI Whisper API."""
        self.transcription: str = ""
        """Current transcription."""

        # Recording settings
        self.recorder.energy_threshold = self.energy_threshold
        self.recorder.dynamic_energy_threshold = False
        self.source: sr.Microphone = self.get_microphone()
        with self.source as source:
            self.recorder.adjust_for_ambient_noise(source)
        # Create a background thread that will pass us raw audio bytes.
        self.recorder.listen_in_background(
            self.source, self._record_callback, phrase_time_limit=self.record_timeout
        )
        print("Transcription ready.")

    def get_microphone(self) -> sr.Microphone:
        """Get speech recognition microphone device"""
        mic_name = self.default_microphone

        # Allow user to pick microphone
        if not mic_name or mic_name == "list":
            print("Available microphone devices are: ")
            microphones = sr.Microphone.list_microphone_names()
            if not microphones:
                raise MicrophoneNotFoundError
            for index, name in enumerate(microphones):
                print(str(index + 1) + ". Microphone:", name)
            mic_idx = input(f"Select microphone number (1-{len(microphones)}): ")
            mic_name = microphones[int(mic_idx) - 1]

        # Get microphone object
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            if mic_name in name:
                return sr.Microphone(sample_rate=16000, device_index=index)
        raise KeyError("No microphone with name", mic_name)

    def _record_callback(self, _: Any, audio: sr.AudioData) -> None:
        """
        Threaded callback function to recieve audio data when recordings finish.
        audio: An AudioData containing the recorded bytes.
        """
        # Grab the raw bytes and push it into the thread safe queue.
        data = audio.get_raw_data()
        self.data_queue.put(data)

    def run(self) -> str:
        # assert self.source is not None, 'Invalid microphone source'
        now = datetime.utcnow()
        # Pull raw recorded audio from the queue.
        if not self.data_queue.empty():
            phrase_complete = False
            # If enough time has passed between recordings, consider the phrase complete.
            # Clear the current working audio buffer to start over with the new data.
            if self.phrase_time and now - self.phrase_time > timedelta(
                seconds=self.phrase_timeout
            ):
                self.last_sample = b""
                phrase_complete = True
            # This is the last time we received new audio data from the queue.
            self.phrase_time = now

            # Concatenate our current audio data with the latest audio data.
            while not self.data_queue.empty():
                data = self.data_queue.get()
                self.last_sample += data

            # Use AudioData to convert the raw data to wav data.
            audio_data = sr.AudioData(
                self.last_sample, self.source.SAMPLE_RATE, self.source.SAMPLE_WIDTH
            )
            wav_data = io.BytesIO(audio_data.get_wav_data())
            text = get_transcription(self.temp_file, wav_data)

            # If we detected a pause between recordings, add a new item to our transcription.
            # Otherwise edit the existing one.
            self.transcription = text
            if phrase_complete:
                return self.transcription
            print("\r" + self.transcription, end="")
            return self.run()
        return ""


def main() -> None:
    transcriber = Transcriber(default_microphone="Microphone (2- Blue Snowball )")
    while True:
        try:
            transcription = transcriber.run()
            if transcription:
                print("\r" + transcription)
            sleep(0.25)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
