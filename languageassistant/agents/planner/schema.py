"""Lesson parsing and formatting schemas"""
import re
from abc import ABC, abstractmethod
from typing import List

from langchain.schema import BaseOutputParser
from pydantic import BaseModel


class Lesson(BaseModel):
    """A list of conversation topics for a lesson plan."""

    topics: List[str]

    def __str__(self) -> str:
        """Converts the lesson to a printable string"""
        lesson = ""
        for i, topic in enumerate(self.topics):
            lesson += f"{i + 1}. {topic}\n"
        return lesson


class BaseLessonOutputParser(BaseOutputParser, ABC):
    """Base lesson plan output parser class"""

    @abstractmethod
    def parse(self, text: str) -> Lesson:
        """Parse into a lesson with a list of topics."""


class LessonOutputParser(BaseLessonOutputParser):
    """Parses LLM lesson into a Lesson object"""

    def parse(self, text: str) -> Lesson:
        """Instructions on how the LLM output should be formatted."""
        topics = [v.strip() for v in re.split(r"\n\d+\. ", text)[1:]]
        return Lesson(topics=topics)

    def get_format_instructions(self) -> str:
        """Instructions on how the LLM output should be formatted."""
        return (
            "Please output the requested list of broad lesson topics starting with the header 'Topics:' "
            "and then followed by a numbered list of topics. "
            "Please include enough general topics that a language teacher could "
            "effectively teach the language for the given skill level. "
            "At the end of your list of topics, say '<END_OF_LIST>'"
        )
