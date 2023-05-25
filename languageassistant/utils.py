import os

import openai


def load_openai_api_key(openai_api_key: str = "") -> None:
    """Load OpenAI API key into OpenAI module"""
    if openai_api_key == "":
        try:
            assert os.getenv("OPENAI_API_KEY") is not None
            assert os.getenv("OPENAI_API_KEY") != ""
            openai.api_key = os.getenv("OPENAI_API_KEY")
        except AssertionError:
            raise Exception(
                "OpenAI API key not found. "
                "Please pass in as argument or "
                "set the `OPENAI_API_KEY` environment variable."
            )
    else:
        openai.api_key = openai_api_key
