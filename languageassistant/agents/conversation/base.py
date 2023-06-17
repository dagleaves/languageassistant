"""Conversation agent abstract base classes"""
from abc import ABC, abstractmethod
from typing import Dict

from langchain.callbacks.manager import Callbacks
from pydantic import BaseModel


class BaseConversationAgent(BaseModel, ABC):
    """Abstract base conversation agent class"""

    @abstractmethod
    def greet(self, inputs: Dict[str, str], callbacks: Callbacks = None) -> str:
        """Start a new conversation about a topic."""

    @abstractmethod
    def speak(self, inputs: Dict[str, str], callbacks: Callbacks = None) -> str:
        """Single atomic reply to last human message."""
