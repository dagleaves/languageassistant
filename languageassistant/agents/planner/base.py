"""Planner agent abstract base classes"""
from abc import ABC, abstractmethod
from typing import Any

from langchain.callbacks.manager import Callbacks
from pydantic import BaseModel

from languageassistant.agents.planner.schema import Lesson


class BasePlannerAgent(BaseModel, ABC):
    """Abstract base planner agent class"""

    @abstractmethod
    def plan(self, inputs: dict, callbacks: Callbacks = None, **kwargs: Any) -> Lesson:
        """Get a lesson plan of topics tailored to user background"""
