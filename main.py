import streamlit as st
from streamlit_chat import message
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain.callbacks import get_openai_callback
from pypdf import PdfReader
from dotenv import load_dotenv
load_dotenv()

# os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# defining LLM and memory
llm = ChatOpenAI(model= 'gpt-4', temperature = 0)
memory = ConversationBufferMemory(return_messages = True)

# defining LLM and memory
llm = ChatOpenAI(model= 'gpt-4', temperature = 0)
memory = ConversationBufferMemory(return_messages = True)

# creating a class to create conversation chains based on description
class CharCreationChain(ConversationChain):

  @classmethod
  def from_description(cls, description ) -> ConversationChain:
    prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(description),
    MessagesPlaceholder(variable_name = "history"),
    HumanMessagePromptTemplate.from_template("{input}")
])
    
    return cls(prompt=prompt, llm=llm, memory = memory)

# creating a char creation chain for reviewer
reviewer_chain = CharCreationChain.from_description("You are a reviewer of a resume. You are reviewing a resume and you want to give feedback to the candidate. \n\n")



def feedback(resume, job, query):
    with open('prompt.txt', 'r') as f:
        template = f.read()
    prompt = PromptTemplate(
        template = template,
        input_variables = ["resume", "job", "query"],
    )
    with get_openai_callback() as callback:
        review_chain = 
