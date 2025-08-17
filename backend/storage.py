# backend/storage.py
import os
import shutil
import uuid
from dotenv import load_dotenv

load_dotenv()
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./data/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_file(uploaded_file) -> str:
    """
    uploaded_file is a starlette UploadFile
    returns saved path
    """
    ext = os.path.splitext(uploaded_file.filename)[1] or ""
    dest = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}{ext}")
    with open(dest, "wb") as f:
        shutil.copyfileobj(uploaded_file.file, f)
    return dest