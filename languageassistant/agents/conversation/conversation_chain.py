from langchain.base_language import BaseLanguageModel
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from languageassistant.agents.conversation import ConversationAgent

SYSTEM_TEMPLATE = (
    "Assistant is a native {language} language teacher."
    "Assistant is designed is to teach students the {language} language "
    "by focusing on a realistic conversation scenarios."
    "Assistant should teach any necessary words and phrases first "
    "as needed for their proficiency, then have the "
    "conversation. Assistant should use the least amount of English "
    "as needed for their proficiency.\n"
)

HUMAN_TEMPLATE = (
    "Conversation topic: {topic}\n\n{history}\nHuman: {human_input}\nAssistant:"
)


def load_conversation_agent(
    llm: BaseLanguageModel,
    system_template: str = SYSTEM_TEMPLATE,
    human_template: str = HUMAN_TEMPLATE,
    verbose: bool = False,
) -> ConversationAgent:
    prompt_template = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template(human_template),
        ]
    )
    memory = ConversationBufferMemory(ai_prefix="Assistant")
    llm_chain = LLMChain(
        llm=llm, prompt=prompt_template, memory=memory, verbose=verbose
    )
    return ConversationAgent(
        llm_chain=llm_chain,
    )


# TODO: memory
