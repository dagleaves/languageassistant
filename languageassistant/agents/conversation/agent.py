"""Conversation agent implementation"""
from typing import Dict, List, Optional

from langchain.callbacks.manager import Callbacks
from langchain.chains import LLMChain

from languageassistant.agents.conversation.base import BaseConversationAgent

GREETING = (
    "What should I know before we start the conversation? Any useful words or phrases?"
)


def validate_inputs(inputs: Dict[str, str]) -> None:
    """
    Ensure conversation agent input dicts contain correct keys

    Parameters
    ----------
    inputs
        Dictionary containing conversation inputs. Expects:

            - language
            - proficiency
            - topic
    """
    assert "language" in inputs, "Must provide target language for conversation agent"
    assert (
        "proficiency" in inputs
    ), "Must provide user target language proficiency for conversation agent"
    assert "topic" in inputs, "Must provide topic for conversation agent"


class ConversationAgent(BaseConversationAgent):
    """LLM agent for conversing about a topic in the target language"""

    llm_chain: LLMChain
    """Any LLM chain for inference"""
    stop: Optional[List] = None
    """LLM end-of-response keyword"""

    def greet(self, inputs: Dict[str, str], callbacks: Callbacks = None) -> str:
        """Start a new conversation about a topic."""
        _inputs = inputs.copy()
        validate_inputs(inputs)
        if "human_input" not in _inputs:
            _inputs["human_input"] = GREETING
        response = self.speak(_inputs)
        return response

    def speak(self, inputs: Dict[str, str], callbacks: Callbacks = None) -> str:
        """
        Get single response to user input

        Parameters
        ----------
        inputs
            Conversation inputs dictionary. Expects:

                - language: target language (optional)
                - proficiency: user proficiency with target language (optional)
                - topic: the topic to discuss (optional)
                - input: the current user input in the conversation
        callbacks
            LangChain LLM callbacks

        Returns
        -------
        str
            Single LLM response
        """
        _inputs = inputs.copy()
        validate_inputs(_inputs)
        assert (
            "human_input" in _inputs
        ), "Must provide human input for conversation chain"
        llm_response = self.llm_chain.run(
            **_inputs, stop=self.stop, callbacks=callbacks
        )
        return llm_response
