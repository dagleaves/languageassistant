import re

from langchain.base_language import BaseLanguageModel
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import SystemMessage

from languageassistant.agents.planner.base import LessonPlanner
from languageassistant.agents.planner.schema import Lesson, LessonOutputParser

SYSTEM_PROMPT = (
    "Please output the requested list of broad lesson topics starting with the header 'Topics:' "
    "and then followed by a numbered list of topics. "
    "Please include enough general topics that a language teacher could "
    "effectively teach the language for the given skill level. "
    "At the end of your list of topics, say '<END_OF_LIST>'"
)

HUMAN_TEMPLATE = (
    "Write a list of lesson topics for a person learning {language} "
    "through immersion by speaking with a native speaker of {language}. "
    "The learner has {proficiency} level experience with {language}. "
    "Tailor the lesson topics for the native instructor "
    "for the level of experience the learner has."
)


class LessonPlanningOutputParser(LessonOutputParser):
    def parse(self, text: str) -> Lesson:
        topics = [v.strip() for v in re.split(r"\n\d+\. ", text)[1:]]
        return Lesson(topics=topics)


def load_lesson_planner(
    llm: BaseLanguageModel, system_prompt: str = SYSTEM_PROMPT, verbose: bool = False
) -> LessonPlanner:
    prompt_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_prompt),
            HumanMessagePromptTemplate.from_template(HUMAN_TEMPLATE),
        ]
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt_template, verbose=verbose)
    return LessonPlanner(
        llm_chain=llm_chain,
        output_parser=LessonPlanningOutputParser(),
        stop=["<END_OF_LIST>"],
    )
