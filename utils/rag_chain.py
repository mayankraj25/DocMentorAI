from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from utils.config_stub import get_config

load_dotenv()
CONF=get_config()
def get_llm():
    if(CONF["LLM_BACKEND"]==openai):
        return ChatOpenAI(model=CONF["LLM_MODEL"], temperature=0.2)
    else:
        return ChatOllama(model=CONF["LLM_MODEL2"],temperature=0.2)

def create_chain_from_retriever(retriever):
    prompt = PromptTemplate.from_template("""
    You are a helpful assistant that answers questions based on the retrieved document chunks.
    {context}
    Question: {question}
    Answer in a concise manner and list source metadata when used.
    """)
    llm=get_llm()
    memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    chain=ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory=memory,combine_docs_chain_kwargs={"prompt": prompt})
    return chain