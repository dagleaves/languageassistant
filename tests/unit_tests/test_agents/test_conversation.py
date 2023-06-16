import os

import pytest
from langchain.chat_models import ChatOpenAI

from languageassistant.agents.conversation import load_conversation_agent
from languageassistant.agents.conversation.base import validate_inputs
from languageassistant.utils import load_openai_api_key

invalid_openai_api_key = os.getenv("OPENAI_API_KEY") in [None, "", "api_key"]


test_inputs = {
    "language": "English",
    "proficiency": "Beginner",
    "topic": "Greetings and Introductions",
}


@pytest.mark.skipif(invalid_openai_api_key, reason="Needs valid OpenAI API key")
def setup_module() -> None:
    load_openai_api_key()


def test_validate_inputs_language_assertion() -> None:
    inputs = {"proficiency": "proficiency", "topic": "topic"}
    with pytest.raises(
        AssertionError, match="Must provide target language for conversation agent"
    ):
        validate_inputs(inputs)


def test_validate_inputs_proficiency_assertion() -> None:
    inputs = {"language": "language", "topic": "topic"}
    with pytest.raises(
        AssertionError,
        match="Must provide user target language proficiency for conversation agent",
    ):
        validate_inputs(inputs)


def test_validate_inputs_topic_assertion() -> None:
    inputs = {"language": "language", "proficiency": "proficiency"}
    with pytest.raises(
        AssertionError, match="Must provide topic for conversation agent"
    ):
        validate_inputs(inputs)


@pytest.mark.skipif(invalid_openai_api_key, reason="Needs valid OpenAI API key")
def test_initialize_conversation_agent() -> None:
    llm = ChatOpenAI(temperature=0)  # type: ignore[call-arg]
    load_conversation_agent(llm)


@pytest.mark.skipif(invalid_openai_api_key, reason="Needs valid OpenAI API key")
def test_conversation_greet() -> None:
    llm = ChatOpenAI(temperature=0)  # type: ignore[call-arg]
    agent = load_conversation_agent(llm)
    agent.greet(test_inputs)


@pytest.mark.skipif(invalid_openai_api_key, reason="Needs valid OpenAI API key")
def test_conversation_speak() -> None:
    llm = ChatOpenAI(temperature=0)  # type: ignore[call-arg]
    agent = load_conversation_agent(llm)
    full_input = test_inputs.copy()
    full_input["human_input"] = "Hello"
    agent.speak(full_input)


@pytest.mark.skipif(invalid_openai_api_key, reason="Needs valid OpenAI API key")
def test_conversation_speak_assertion() -> None:
    llm = ChatOpenAI(temperature=0)  # type: ignore[call-arg]
    agent = load_conversation_agent(llm)
    print(test_inputs)
    with pytest.raises(
        AssertionError, match="Must provide human input for conversation chain"
    ):
        agent.speak(test_inputs)
