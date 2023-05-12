import os


def check_openai_import() -> None:
    """Ensure openai library is installed"""
    try:
        pass
    except ImportError:
        raise ImportError(
            "Module `openai` not found." "Please install with `pip install openai`"
        )


def load_openai_api_key(openai_api_key: str = "") -> None:
    """Load OpenAI API key into OpenAI module"""
    check_openai_import()
    import openai

    if openai_api_key == "":
        try:
            assert os.getenv("OPENAI_API_KEY") is not None
            openai.api_key = os.getenv("OPENAI_API_KEY")
        except AssertionError:
            raise Exception(
                "OpenAI API key not found."
                "Please pass in as argument or"
                "set the `OPENAI_API_KEY` environment variable."
            )
    else:
        openai.api_key = openai_api_key
