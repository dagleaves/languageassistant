from abc import abstractmethod
from typing import List

from langchain.schema import BaseOutputParser
from pydantic import BaseModel


class Topic(BaseModel):
    """Conversation topic."""

    value: str

    def __str__(self) -> str:
        return self.value


class Lesson(BaseModel):
    """A list of conversation topics for a lesson plan."""

    topics: List[Topic]

    def __str__(self) -> str:
        lesson = ""
        for i, topic in enumerate(self.topics):
            lesson += f"{i + 1}. {topic}\n"
        return lesson


class LessonOutputParser(BaseOutputParser):
    @abstractmethod
    def parse(self, text: str) -> Lesson:
        """Parse into a lesson with a list of topics."""
