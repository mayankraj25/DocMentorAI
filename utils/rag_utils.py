import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_DIR=os.getenv("CHROMA_DIR", "vectorstore")

def split_documents(docs):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=100)
    return text_splitter.split_documents(docs)

def get_embeddings():
    return HuggingFaceEmbeddings(model_name=os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"))

def get_vectorstore():
    return Chroma(persist_directory=CHROMA_DIR,embedding_function=get_embeddings())
