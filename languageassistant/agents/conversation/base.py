from abc import abstractmethod
from typing import Dict, List, Optional

from langchain.callbacks.manager import Callbacks
from langchain.chains.llm import LLMChain
from pydantic import BaseModel

GREETING = (
    "What should I know before we start the conversation? Any useful words or phrases?"
)


def validate_inputs(inputs: Dict[str, str]) -> None:
    assert "language" in inputs, "Must provide target language for conversation agent"
    assert (
        "proficiency" in inputs
    ), "Must provide user target language proficiency for conversation agent"
    assert "topic" in inputs, "Must provide topic for conversation agent"


class BaseConversationAgent(BaseModel):
    @abstractmethod
    def greet(self, inputs: Dict[str, str], callbacks: Callbacks = None) -> str:
        """Start a new conversation about a topic."""

    @abstractmethod
    def speak(self, inputs: Dict[str, str], callbacks: Callbacks = None) -> str:
        """Single atomic reply to last human message."""


class ConversationAgent(BaseConversationAgent):
    llm_chain: LLMChain
    stop: Optional[List] = None

    def greet(self, inputs: Dict[str, str], callbacks: Callbacks = None) -> str:
        """Start a new conversation about a topic."""
        validate_inputs(inputs)
        if "human_input" not in inputs:
            inputs["human_input"] = GREETING
        response = self.speak(inputs)
        return response

    def speak(self, inputs: Dict[str, str], callbacks: Callbacks = None) -> str:
        """Given input, create reply.
        inputs: dict {
        langauge: target language (optional),
        proficiency: user proficiency with target language (optional)
        topic: the topic to discuss (optional),
        input: the current user input in the conversation
        """
        validate_inputs(inputs)
        assert (
            "human_input" in inputs
        ), "Must provide human input for conversation chain"
        llm_response = self.llm_chain.run(**inputs, stop=self.stop, callbacks=callbacks)
        return llm_response
