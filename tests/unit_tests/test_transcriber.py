import openai

from languageassistant.transcriber import Transcriber, load_openai


def test_openai_apikey() -> None:
    load_openai()
    assert openai.api_key != ""


def test_transcriber_initialization() -> None:
    Transcriber()
