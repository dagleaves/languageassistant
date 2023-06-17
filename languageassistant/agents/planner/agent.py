"""Lesson planning agent implementation"""
from typing import Any, List, Optional

from langchain.callbacks.manager import Callbacks
from langchain.chains import LLMChain

from languageassistant.agents.planner.base import BasePlannerAgent
from languageassistant.agents.planner.schema import Lesson, LessonOutputParser


class LessonPlannerAgent(BasePlannerAgent):
    """LLM agent for planning language lessons"""

    llm_chain: LLMChain
    output_parser: LessonOutputParser
    stop: Optional[List] = None

    def plan(self, inputs: dict, callbacks: Callbacks = None, **kwargs: Any) -> Lesson:
        """Get a lesson plan of topics tailored to user background"""
        llm_response = self.llm_chain.run(**inputs, stop=self.stop, callbacks=callbacks)
        return self.output_parser.parse(llm_response)
