import io
from tempfile import NamedTemporaryFile

import openai
import pytest
import speech_recognition as sr
from pytest import MonkeyPatch

from languageassistant.transcriber import Transcriber, get_transcription

microphones = sr.Microphone.list_microphone_names()
has_microphone = len(microphones) > 0


@pytest.mark.skipif(not has_microphone, reason="No microphone available")
def test_transcriber_initialization(monkeypatch: MonkeyPatch) -> None:
    print(type(monkeypatch))
    monkeypatch.setattr("builtins.input", lambda _: 1)
    Transcriber()


def test_get_transcription_too_short() -> None:
    temp_file = NamedTemporaryFile(suffix=".wav").name
    audio_data = sr.AudioData(b"", 16000, 2)
    wav_data = io.BytesIO(audio_data.get_wav_data())
    with pytest.raises(openai.error.InvalidRequestError):
        get_transcription(temp_file, wav_data)


def test_get_transcription_null_bytes() -> None:
    temp_file = NamedTemporaryFile(suffix=".wav").name
    audio_bytes = bytes([0 for _ in range(3500)])
    audio_data = sr.AudioData(audio_bytes, 16000, 2)
    wav_data = io.BytesIO(audio_data.get_wav_data())
    get_transcription(temp_file, wav_data)


def test_get_microphone_invalid_name(monkeypatch: MonkeyPatch) -> None:
    with pytest.raises(KeyError):
        Transcriber(default_microphone="invalid")


def test_transcriber_run_empty(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: 1)
    transcriber = Transcriber()
    transcription = transcriber.run()
    assert transcription is None
