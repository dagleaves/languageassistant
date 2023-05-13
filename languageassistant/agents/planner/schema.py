from abc import abstractmethod
from typing import List

from langchain.schema import BaseOutputParser
from pydantic import BaseModel


class Topic(BaseModel):
    """Conversation topic."""

    value: str


class Lesson(BaseModel):
    """A list of conversation topics for a lesson plan."""

    topics: List[Topic]


class LessonOutputParser(BaseOutputParser):
    @abstractmethod
    def parse(self, text: str) -> Lesson:
        """Parse into a lesson with a list of topics."""
