import re

from langchain.base_language import BaseLanguageModel
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import SystemMessage

from languageassistant.agents.planner.base import LessonPlanner
from languageassistant.agents.planner.schema import Lesson, LessonOutputParser, Topic

SYSTEM_PROMPT = (
    "Let's first understand the problem and devise a plan to solve the problem."
    "Please output the requested list of conversation topics starting with the header 'Lesson:' "
    "and then followed by a numbered list of topics. "
    "Please make the plan the minimum number of topics required "
    "to effectively teach the language for the given skill level."
    "At the end of your list of topics, say '<END_OF_LESSON>'"
)

HUMAN_TEMPLATE = (
    "Write a list of conversation topics for a person learning {language} "
    "through immersion by speaking with a native speaker of {language}."
    "The learner has {proficiency} level experience with {language}."
    "Tailor the conversations and lessons for the native instructor "
    "for the level of experience the learner has."
)


class LessonPlanningOutputParser(LessonOutputParser):
    def parse(self, text: str) -> Lesson:
        topics = [Topic(value=v) for v in re.split("\n\\d+\\. ", text)[1:]]
        return Lesson(topics=topics)


def load_lesson_planner(
    llm: BaseLanguageModel, system_prompt: str = SYSTEM_PROMPT
) -> LessonPlanner:
    prompt_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_prompt),
            HumanMessagePromptTemplate.from_template(HUMAN_TEMPLATE),
        ]
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt_template)
    return LessonPlanner(
        llm_chain=llm_chain,
        output_parser=LessonPlanningOutputParser(),
        stop=["<END_OF_LESSON>"],
    )
