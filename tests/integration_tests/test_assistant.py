import os

import pytest
import speech_recognition as sr

from languageassistant.agents.planner.schema import Lesson
from languageassistant.assistant import Assistant
from languageassistant.transcriber import Transcriber
from languageassistant.tts import TTS

no_google_api_key = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") in [None, "", "api_key"]
microphones = sr.Microphone.list_microphone_names()
invalid_openai_api_key = os.getenv("OPENAI_API_KEY") in [None, "", "api_key"]


@pytest.mark.skipif(
    not microphones or invalid_openai_api_key or no_google_api_key,
    reason="Needs microphones and valid OpenAI API and Google API keys",
)
def test_conversation_with_tts() -> None:
    """Test only conversation loop with tts enabled"""
    language = "English"
    proficiency = "Fluent"

    transcriber = Transcriber(default_microphone="Microphone (Blue Snowball )")
    tts = TTS(language=language)
    lesson = Lesson(topics=["Greetings and Introductions"])
    assistant = Assistant(
        language=language,
        proficiency=proficiency,
        lesson=lesson,
        transcriber=transcriber,
        tts=tts,
    )
    assistant.converse(topic="Greetings and Introductions")


@pytest.mark.skipif(
    not microphones or invalid_openai_api_key or no_google_api_key,
    reason="Needs microphones and valid OpenAI API and Google API keys",
)
def test_assistant_plan_lesson() -> None:
    """Test assistant plan lesson method"""
    language = "English"
    proficiency = "Fluent"

    transcriber = Transcriber(default_microphone="Microphone (Blue Snowball )")
    tts = TTS(language=language)
    assistant = Assistant(
        language=language, proficiency=proficiency, transcriber=transcriber, tts=tts
    )
    assistant.plan_lesson()
    assert len(assistant.lesson.topics) > 0


@pytest.mark.skipif(
    not microphones or invalid_openai_api_key or no_google_api_key,
    reason="Needs microphones and valid OpenAI API and Google API keys",
)
def test_assistant_greet() -> None:
    """Test assistant greet method"""
    language = "English"
    proficiency = "Fluent"

    transcriber = Transcriber(default_microphone="Microphone (Blue Snowball )")
    tts = TTS(language=language)
    assistant = Assistant(
        language=language, proficiency=proficiency, transcriber=transcriber, tts=tts
    )
    greeting = assistant.greet("Respond with only the word Hello")
    assert greeting != ""


@pytest.mark.skipif(
    not microphones or invalid_openai_api_key or no_google_api_key,
    reason="Needs microphones and valid OpenAI API and Google API keys",
)
def test_assistant_output_topic_background() -> None:
    """Test assistant topic background output method"""
    language = "English"
    proficiency = "Fluent"

    transcriber = Transcriber(default_microphone="Microphone (Blue Snowball )")
    tts = TTS(language=language)
    assistant = Assistant(
        language=language, proficiency=proficiency, transcriber=transcriber, tts=tts
    )
    assistant._output_topic_background("Respond with only the word Hello")
