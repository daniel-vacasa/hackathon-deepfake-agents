import openai
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
import os


prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know."),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])


llm = ChatOpenAI(temperature=0, openai_api_key=os.environ.get("OPENAI_API_KEY"))
memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)


def rewrite_in_style(prompt, style):
    _prompt = f"""

    Rewrite the following text in the style of {style}: 
    
    {prompt}
    
    """

    response = conversation.predict(input=_prompt)

    return response

def give_feedback(prompt, style):
    _prompt = f"""

    Give feedback on the following text description - is it clear? Is everything important included? Speak in the style of {style}: 
    
    {prompt}
    
    """

    response = conversation.predict(input=_prompt)

    return response