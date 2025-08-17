from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from backend.db import SessionLocal, init_db, User
from backend.auth import hash_password, verify_password, create_access_token, decode_token
from backend.storage import save_uploaded_file
from backend.indexer import index_file
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os
from dotenv import load_dotenv

init_db()

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

class RegisterIn(BaseModel):
    username: str
    password: str

class LoginIn(BaseModel):
    username: str
    password: str

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register")
def register(payload: RegisterIn,db=Depends(get_db)):
    user=db.query(User).filter(User.userName==payload.username).first()
    if(user):
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password=hash_password(payload.password)
    new_user=User(username=payload.username,hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status": "registered"}

@app.post("/login")
def login(payload: LoginIn, db=Depends(get_db)):
    user=db.query(User).filter(User.username==payload.username).first()
    if not user or not verify_password(payload.password,user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token=create_access_token(sub=user.username)
    return {"access_token": token, "token_type": "bearer"}

def require_user(token: str = None):
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    try:
        payload = decode_token(token)
        return payload["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    
@app.post("/upload")
def upload_doc(file: UploadFile = File(...), background_tasks: BackgroundTasks = None, token: str | None = None):
    # simple optional auth check
    if token:
        require_user(token)
    # save file
    saved = save_uploaded_file(file)
    # start background indexing
    if background_tasks:
        background_tasks.add_task(index_file, saved)
        return {"status": "indexing_started", "path": saved}
    else:
        result = index_file(saved)
        return result
    
class ChatIn(BaseModel):
    question: str
    persist_dir: str

@app.post("/chat")
def chat_endpoint(payload: ChatIn, token: str):
    if token:
        require_user(token)
    from utils.vectorstore import load_vectorstore
    from utils.rag_chain import create_chain_from_retriever
    persist = payload.persist_dir or os.getenv("CHROMA_DIR", "./vectorstore/chroma_store")
    db = load_vectorstore(persist)
    retriever = db.as_retriever(search_kwargs={"k": 3})
    chain = create_chain_from_retriever(retriever)
    resp = chain({"question": payload.question})
    # return answer & any retrieved docs metadata
    return {"answer": resp.get("answer"), "source_documents": [d.metadata for d in resp.get("source_documents", [])]}