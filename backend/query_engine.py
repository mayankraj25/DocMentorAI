from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from utils.rag_utils import get_vectorstore
from langchain.chains import RetrievalQA

def query_documents(question,vectordb=None):
    if not vectordb:
        vectordb=get_vectorstore()

    retriever=vectordb.as_retriever(search_kwargs={"k":5})
    prompt = PromptTemplate.from_template("""
You are a document assistant. Answer the question below using only the context provided.

Context:
{context}

Question: {question}

Helpful Answer:
""")
    
    chain=RetrievalQA.from_chain_type(
        llm=ChatOllama(model='llama3',temperature=0.1),
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )
    return chain.run(question)

