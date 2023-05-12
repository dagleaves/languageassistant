import os

import openai
import pytest

from languageassistant.utils import load_openai_api_key


def test_openai_api_key_env_success() -> None:
    load_openai_api_key()
    assert openai.api_key != ""


def test_openai_api_key_env_fail() -> None:
    with pytest.raises(Exception, match=r"OpenAI API key not found."):
        os.environ.pop("OPENAI_API_KEY", None)
        load_openai_api_key()


def test_openai_api_key_string_success() -> None:
    load_openai_api_key("api_key")
    assert openai.api_key != ""
