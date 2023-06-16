"""Fully integrated language assistant"""
import time
from typing import Dict, List, Optional

import questionary
from langchain.base_language import BaseLanguageModel
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel

from languageassistant.agents.conversation import (
    BaseConversationAgent,
    load_conversation_agent,
)
from languageassistant.agents.planner import (
    BasePlannerAgent,
    Lesson,
    load_lesson_planner,
)
from languageassistant.transcriber import Transcriber
from languageassistant.tts import TTS


class Assistant(BaseModel):
    """Full language assistant model"""

    language: str
    proficiency: str
    lesson: Lesson = Lesson(topics=[])

    llm: BaseLanguageModel = ChatOpenAI(temperature=0)  # type: ignore[call-arg]
    lesson_agent: BasePlannerAgent = load_lesson_planner(llm)
    conversation_agent: BaseConversationAgent = load_conversation_agent(llm)
    transcriber: Transcriber
    tts: TTS
    use_tts: bool = True

    class Config:
        arbitrary_types_allowed = True

    @property
    def background(self) -> Dict[str, str]:
        return {"language": self.language, "proficiency": self.proficiency}

    def plan_lesson(self) -> None:
        """Plan a lesson for the target language using user's background"""
        self.lesson = self.lesson_agent.plan(self.background)

    def greet(self, topic: str) -> str:
        """Receive background teaching about a topic"""
        inputs = self.background.copy()
        inputs["topic"] = topic
        return self.conversation_agent.greet(inputs)

    def speak(self, topic: str, human_input: str) -> str:
        """Single response from user's conversation input"""
        inputs = self.background.copy()
        inputs["topic"] = topic
        inputs["human_input"] = human_input
        return self.conversation_agent.speak(inputs)

    def converse(self, topic: str) -> None:
        """Converse with conversation agent about a topic"""
        try:
            while True:
                print("Microphone recording...", end="")
                user_input = self.transcriber.run()
                if user_input == "":
                    print("\r", end="")
                    time.sleep(0.25)
                    continue
                r_padding = " " * max(
                    23 - 7 - len(user_input), 0
                )  # fully cover "Microphone recording..."
                print("\rHuman:", user_input, r_padding)
                print("Retrieving response...", end="")
                ai_response = self.speak(topic, user_input)
                if "<END_CONVERSATION>" in ai_response:
                    return
                print("\rAssistant:", ai_response)
                if self.use_tts:
                    self.tts.run(ai_response)
        except KeyboardInterrupt:
            return

    def _output_topic_background(self, topic: str) -> None:
        """Output topic background teaching"""
        print("Retrieving topic background teaching...")
        topic_prereqs = self.greet(topic)
        print(topic_prereqs)
        if self.use_tts:
            self.tts.run(topic_prereqs)

    def run(
        self, include_topic_background: bool, lesson: Optional[List[str]] = None
    ) -> None:
        """Full assistant discussion loop
        @param include_topic_background: if assistant should explain topic before conversing
        @param lesson: custom list of topics for lesson
        @return None
        """
        # Get lesson plan if not provided
        if lesson is None:
            self.plan_lesson()
        else:
            self.lesson = Lesson(topics=lesson)

        # Display topics
        print("List of conversation topics:")
        print(self.lesson)

        # TODO: Allow user to provide feedback to adjust topics (too easy, too hard, done before)
        # Can probably use regular LLM for this?

        # Begin lesson
        for topic in self.lesson.topics:
            print("Starting new conversation. Press CTRL + C to end conversation")
            print("Topic:", topic)
            if include_topic_background:
                self._output_topic_background(topic)
            self.converse(topic)

            # Continue to next topic or return
            if topic == self.lesson.topics[-1]:  # No more topics -> return
                return
            continue_conversations = questionary.select(
                "Conversation ended. Continue to next topic?",
                choices=[
                    "Yes",
                    "No",
                ],
            ).ask()
            if continue_conversations == "No":
                return
