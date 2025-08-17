import os
import tempfile
from utils.config_stub import get_config
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()
CONF=get_config()
def get_embeddings():
    if(CONF["EMBEDDING_BACKEND"] == "openai"):
        return OpenAIEmbeddings(model=CONF["EMBEDDING_MODEL"])
    else:
        return HuggingFaceEmbeddings(model_name=CONF["EMBEDDING_MODEL2"])
    
def build_vectorstore_from_documents(docs:List[Document],persist_dir:str):
    embeddings= get_embeddings()
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    chunks=[]
    for d in docs:
        pieces = splitter.split_text(d.page_content)
        for i, p in enumerate(pieces):
            meta = dict(d.metadata or {})
            meta.update({"source_page": meta.get("page"), "chunk_index": i})
            chunks.append(Document(page_content=p, metadata=meta))
    embeddings = get_embeddings()
    os.makedirs(persist_dir, exist_ok=True)
    db = Chroma.from_documents(chunks, embedding_function=embeddings, persist_directory=persist_dir)
    db.persist()
    return db


def load_vectorstore(persist_dir:str):
    embeddings=get_embeddings()
    return Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )