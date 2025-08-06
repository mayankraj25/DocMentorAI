from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate

def summarize_text(text):
    prompt= PromptTemplate.from_template("""
Summarize the following document in clear bullet points:

{text}
""")
    
    llm=ChatOllama(model="llama3",temperature=0.1)
    return llm.invoke(prompt.format(text=text)).content.strip()
