"""Project-wide utils"""
import os

import openai

supported_languages = ["English", "Spanish", "Chinese"]

country_codes = {"English": "en-US", "Chinese": "cmn-CN", "Spanish": "es-ES"}


def load_openai_api_key(openai_api_key: str = "") -> None:
    """Load OpenAI API key into OpenAI module"""
    if openai_api_key == "":
        try:
            assert os.getenv("OPENAI_API_KEY") is not None
            assert os.getenv("OPENAI_API_KEY") != ""
            openai.api_key = os.getenv("OPENAI_API_KEY")
        except AssertionError as exc:
            raise KeyError(
                "OpenAI API key not found. "
                "Please pass in as argument or "
                "set the `OPENAI_API_KEY` environment variable."
            ) from exc
    else:
        openai.api_key = openai_api_key
