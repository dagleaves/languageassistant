from langchain.chat_models import ChatOpenAI

from languageassistant.agents.planner import load_lesson_planner
from languageassistant.agents.planner.schema import Lesson
from languageassistant.utils import load_openai_api_key


def setup_module() -> None:
    load_openai_api_key()


def test_schema_empty_lesson_repr() -> None:
    test_lesson = Lesson(topics=[])
    assert str(test_lesson) == ""


def test_schema_lesson_repr() -> None:
    test_lesson = Lesson(topics=["test"])
    assert str(test_lesson) == "1. test\n"


def test_initialize_planner() -> None:
    llm = ChatOpenAI(temperature=0)  # type: ignore[call-arg]
    load_lesson_planner(llm)


def test_planner_result() -> None:
    llm = ChatOpenAI(temperature=0)  # type: ignore[call-arg]
    agent = load_lesson_planner(llm)
    inputs = {
        "language": "Chinese",
        "proficiency": "Beginner",
    }
    agent.plan(inputs)
