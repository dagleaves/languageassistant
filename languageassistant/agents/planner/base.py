from abc import abstractmethod
from typing import Any, List, Optional

from langchain.callbacks.manager import Callbacks
from langchain.chains.llm import LLMChain
from pydantic import BaseModel

from languageassistant.agents.planner.schema import Lesson, LessonOutputParser


class BasePlanner(BaseModel):
    @abstractmethod
    def plan(self, inputs: dict, callbacks: Callbacks = None, **kwargs: Any) -> Lesson:
        """Given input, decided what to do."""

    @abstractmethod
    async def aplan(
        self, inputs: dict, callbacks: Callbacks = None, **kwargs: Any
    ) -> Lesson:
        """Given input, decided what to do."""


class LessonPlanner(BasePlanner):
    llm_chain: LLMChain
    output_parser: LessonOutputParser
    stop: Optional[List] = None

    def plan(self, inputs: dict, callbacks: Callbacks = None, **kwargs: Any) -> Lesson:
        """Given input, decided what to do."""
        llm_response = self.llm_chain.run(**inputs, stop=self.stop, callbacks=callbacks)
        return self.output_parser.parse(llm_response)

    async def aplan(
        self, inputs: dict, callbacks: Callbacks = None, **kwargs: Any
    ) -> Lesson:
        """Given input, decided what to do."""
        llm_response = await self.llm_chain.arun(
            **inputs, stop=self.stop, callbacks=callbacks
        )
        return self.output_parser.parse(llm_response)
