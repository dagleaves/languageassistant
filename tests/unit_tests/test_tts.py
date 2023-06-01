from languageassistant.tts import TTS


def test_tts_init() -> None:
    TTS(language="English")


def test_tts_playback() -> None:
    tts = TTS(language="English")
    tts.run("Hello, world.")
