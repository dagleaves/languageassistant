import io
import os
from tempfile import NamedTemporaryFile

import openai
import pytest
import speech_recognition as sr
from pytest import MonkeyPatch

from languageassistant.transcriber import Transcriber, get_transcription

microphones = sr.Microphone.list_microphone_names()
invalid_openai_api_key = os.getenv("OPENAI_API_KEY") in [None, "", "api_key"]


@pytest.mark.skipif(
    not microphones or invalid_openai_api_key,
    reason="Needs microphones and valid OpenAI API key",
)
def test_transcriber_initialization(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: 1)
    Transcriber()


@pytest.mark.skipif(invalid_openai_api_key, reason="Needs valid OpenAI API key")
def test_get_transcription_too_short() -> None:
    temp_file = NamedTemporaryFile(suffix=".wav").name
    audio_data = sr.AudioData(b"", 16000, 2)
    wav_data = io.BytesIO(audio_data.get_wav_data())
    with pytest.raises(openai.error.InvalidRequestError):
        get_transcription(temp_file, wav_data)


@pytest.mark.skipif(invalid_openai_api_key, reason="Needs valid OpenAI API key")
def test_get_transcription_null_bytes() -> None:
    temp_file = NamedTemporaryFile(suffix=".wav").name
    audio_bytes = bytes([0 for _ in range(3500)])
    audio_data = sr.AudioData(audio_bytes, 16000, 2)
    wav_data = io.BytesIO(audio_data.get_wav_data())
    get_transcription(temp_file, wav_data)


@pytest.mark.skipif(
    not microphones or invalid_openai_api_key,
    reason="Needs microphones and valid OpenAI API key",
)
def test_transcriber_run_empty(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: 1)
    transcriber = Transcriber()
    transcription = transcriber.run()
    assert transcription == ""


@pytest.mark.skipif(
    not microphones or invalid_openai_api_key,
    reason="Needs microphones and valid OpenAI API key",
)
def test_transcriber_run_nonempty(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: 1)
    transcriber = Transcriber()
    test_wav_audio = b"\x00\x00\x00\x00"
    transcriber.data_queue.put(test_wav_audio)
    with pytest.raises(
        openai.error.InvalidRequestError,
        match="Audio file is too short. Minimum audio length is 0.1 seconds.",
    ):
        transcriber.run()


@pytest.mark.skipif(invalid_openai_api_key, reason="Needs valid OpenAI API key")
def test_get_microphone_invalid_name() -> None:
    with pytest.raises(KeyError):
        Transcriber(default_microphone="invalid")
