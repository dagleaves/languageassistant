from languageassistant.agents.planner.schema import Lesson, Topic


def test_schema_topic_repr() -> None:
    test_topic = Topic(value="test")
    assert test_topic.value == str(test_topic)


def test_schema_empty_lesson_repr() -> None:
    test_lesson = Lesson(topics=[])
    assert str(test_lesson) == "Lesson:\n"


def test_schema_lesson_repr() -> None:
    test_topic = Topic(value="test")
    test_lesson = Lesson(topics=[test_topic])
    assert str(test_lesson) == "Lesson:\n1. test\n"
