import os
from dotenv import load_dotenv
load_dotenv()
def get_config():
    return {
        "EMBEDDING_BACKEND": os.getenv("EMBEDDING_BACKEND", "openai"),
        "EMBEDDING_MODEL": os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
        "EMBEDDING_MODEL2": os.getenv("EMBEDDING_MODEL2", "all-MiniLM-L6-v2"),
        "CHROMA_DIR": os.getenv("CHROMA_DIR", "./vectorstore/chroma_store"),
        "LLM_BACKEND": os.getenv("LLM_BACKEND","openai"),
        "LLM_MODEL": os.getenv("LLM_MODEL","gpt-4o-mini"),
        "LLM_MODEL2": os.getenv("LLM_MODEL2","llama3"),
    }