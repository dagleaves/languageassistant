import os

import pytest

from languageassistant.tts import TTS

no_google_api_key = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") in [None, "", "api_key"]


@pytest.mark.skipif(
    no_google_api_key, reason="Needs microphones and valid OpenAI API key"
)
def test_tts_init() -> None:
    TTS(language="English")


@pytest.mark.skipif(
    no_google_api_key, reason="Needs microphones and valid OpenAI API key"
)
def test_tts_playback() -> None:
    tts = TTS(language="English")
    tts.run("Hello, world.")
