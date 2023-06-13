import streamlit as st
from streamlit_chat import message

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, ConversationChain
from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)
from langchain.chains.conversation.memory import ConversationBufferMemory
import PyPDF2

import os
# from dotenv import load_dotenv
# load_dotenv()

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

with open("initial_review_template.txt", "r") as f:
    initial_review_template = f.read()

with open("query_template.txt", "r") as f:
    query_template = f.read()
# print(query_template)

def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    num_pages = len(reader.pages)
    text = ''
    for i in range(num_pages):
        page = reader.pages[i]
        text += page.extract_text()

    return text

# defining LLM
llm = ChatOpenAI(model= 'gpt-3.5-turbo', temperature = 0)


# for initial review
initial_review_prompt = PromptTemplate(input_variables = ["resume", "job_description"], template = initial_review_template)

def get_initial_review(resume, job_description):
    initial_review_chain = LLMChain(prompt = initial_review_prompt, llm = llm)
    return initial_review_chain.run({"resume": resume, "job_description": job_description})

# for query
## find a way to add responses from initial review chain to create query_chain with memory

memory = ConversationBufferMemory(return_messages = True)

def create_query_prompt(resume, job_description):
    query_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(query_template.format(resume = resume, job_description = job_description )),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")])
    return query_prompt





def main():
    st.title("Smart Resume Reviewer! 🤖")
    st.markdown("📄 Upload your resume and job role to get feedback")

    resume_pdf = st.file_uploader("Upload your resume", type = ["pdf"], label_visibility= "collapsed")
    job_description = st.text_input("Enter the role for which you are applying")


    if "initial_review" not in st.session_state:
        st.session_state.initial_review = ""
        
    if "expert_chat" not in st.session_state:
        st.session_state.expert_chat = False

    if "response" not in st.session_state:
        st.session_state.response = ""

    if resume_pdf and job_description:
        resume = read_pdf(resume_pdf)
        st.session_state.initial_review = get_initial_review(resume, job_description)

        query_prompt = create_query_prompt(resume, job_description)
        query_chain = ConversationChain(prompt = query_prompt, llm = llm, memory = memory)

        st.write(st.session_state.initial_review)

        if st.session_state.initial_review != "":
            if st.button("Ask an Expert"):
                st.session_state.expert_chat = True

            if st.session_state.expert_chat:
                query = st.text_input("Enter your query", placeholder= "enter your query", label_visibility= "collapsed")
                if query:
                    # st.write(query)
                    st.write(query_chain.predict(input = query))
                    # st.session_state.response = query_chain.predict(input = query)
    
    # st.write(st.session_state.response)
    

if __name__ == "__main__":
    main()


