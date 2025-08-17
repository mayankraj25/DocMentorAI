# backend/indexer.py
from utils.loader import load_document_by_path
from utils.vectorstore import build_vectorstore_from_documents
from dotenv import load_dotenv
from utils.config_stub import get_config
load_dotenv()
CONF = get_config()

def index_file(path: str, persist_dir: str = None):
    docs = load_document_by_path(path)
    persist = persist_dir or CONF["CHROMA_DIR"]
    db = build_vectorstore_from_documents(docs, persist)
    return {"status": "ok", "persist_dir": persist, "num_docs": len(docs)}