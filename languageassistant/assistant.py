import time
from typing import Dict

import questionary
from langchain.base_language import BaseLanguageModel
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel

from languageassistant.agents.conversation import load_conversation_agent
from languageassistant.agents.conversation.base import BaseConversationAgent
from languageassistant.agents.planner import load_lesson_planner
from languageassistant.agents.planner.base import BasePlanner
from languageassistant.agents.planner.schema import Lesson
from languageassistant.transcriber import Transcriber
from languageassistant.tts import TTS


class Assistant(BaseModel):
    language: str
    proficiency: str
    lesson: Lesson = Lesson(topics=[])

    llm: BaseLanguageModel = ChatOpenAI(temperature=0)  # type: ignore[call-arg]
    lesson_agent: BasePlanner = load_lesson_planner(llm)
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

    def run(self) -> None:
        # Get lesson plan
        self.plan_lesson()

        # Display suggested topics
        print("Suggested list of conversation topics:")
        print(self.lesson)

        # TODO: Allow user to provide feedback to adjust topics (too easy, too hard, done before)
        # Can probably use regular LLM for this?

        # Begin lesson
        for topic in self.lesson.topics:
            print("Starting new conversation. Press CTRL + C to end conversation")
            print("Topic:", topic)
            print("Retrieving topic background teaching...")
            topic_prereqs = self.greet(topic)
            print(topic_prereqs)
            if self.use_tts:
                self.tts.run(topic_prereqs)

            # TODO: Allow user to ask any questions -> enter QA subrouttine then return here when good
            # Maybe need QA Agent?

            try:
                while True:
                    print("Microphone recording...", end="")
                    user_input = self.transcriber.run()
                    if user_input == "":
                        time.sleep(0.25)
                        continue
                    print("\rHuman:", user_input)
                    print("Retrieving response...", end="")
                    ai_response = self.speak(topic, user_input)
                    if "<END_CONVERSATION>" in ai_response:
                        raise KeyboardInterrupt
                    print("\rAssistant:", ai_response)
                    if self.use_tts:
                        self.tts.run(ai_response)
            except KeyboardInterrupt:
                continue_conversation = questionary.select(
                    "Conversation ended. Continue to next topic?",
                    choices=[
                        "Yes",
                        "No",
                    ],
                ).ask()
                if continue_conversation == "No":
                    return
                continue
