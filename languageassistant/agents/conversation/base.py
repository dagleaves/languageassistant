from abc import abstractmethod
from typing import Any, List, Optional

from langchain.callbacks.manager import Callbacks
from langchain.chains.llm import LLMChain
from pydantic import BaseModel


class BaseConversationAgent(BaseModel):
    @abstractmethod
    def speak(self, inputs: dict, callbacks: Callbacks = None, **kwargs: Any) -> str:
        """Given input, create reply."""

    @abstractmethod
    async def aspeak(
        self, inputs: dict, callbacks: Callbacks = None, **kwargs: Any
    ) -> str:
        """Given input, create reply."""


class ConversationAgent(BaseConversationAgent):
    llm_chain: LLMChain
    stop: Optional[List] = None

    def speak(self, inputs: dict, callbacks: Callbacks = None, **kwargs: Any) -> str:
        """Given input, create reply."""
        llm_response = self.llm_chain.run(**inputs, stop=self.stop, callbacks=callbacks)
        return llm_response

    async def aspeak(
        self, inputs: dict, callbacks: Callbacks = None, **kwargs: Any
    ) -> str:
        """Given input, create reply."""
        llm_response = await self.llm_chain.arun(
            **inputs, stop=self.stop, callbacks=callbacks
        )
        return llm_response
