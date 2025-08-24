import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader,TextLoader,Docx2txtLoader
from utils.rag_utils import split_documents,get_embeddings
from langchain.vectorstores import Chroma

CHROMA_DIR=os.getenv("CHROMA_DIR","vectorstore")

def ingest_documents(uploaded_files):
    all_docs=[]
    raw_texts=[]
    for file in uploaded_files:
        suffix=file.name.split('.')[-1].lower()
        with tempfile.NamedTemporaryFile(delete=False,suffix=f".{suffix}") as tmp:
            tmp.write(file.read())
            tmp_path=tmp.name

        if suffix=='pdf':
            loader=PyPDFLoader(tmp_path)
        elif suffix in ['txt','text']:
            loader=TextLoader(tmp_path)
        elif suffix=='docx':
            loader=Docx2txtLoader(tmp_path)
        else:
            continue

        docs=loader.load()
        all_docs.extend(docs)
        for doc in docs:
            raw_texts.append(doc.page_content)

        os.remove(tmp_path)

    if not all_docs:
        return "No valid documents found."
    
    chunks=split_documents(all_docs)
    vectordb=Chroma.from_documents(documents=chunks, embedding=get_embeddings(),persist_directory=CHROMA_DIR)
    combined_text = "\n\n".join(raw_texts)
    return vectordb, combined_text