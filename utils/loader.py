from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredPowerPointLoader
from pdf2image import convert_from_path
from langchain_core.documents import Document
import pytesseract
from typing import List
import tempfile
import os

def load_pdf_pages(path: str)->List[Document]:
    loader= PyPDFLoader(path)
    return loader.load()

def load_docs(path: str)->List[Document]:
    loader= Docx2txtLoader(path)
    return loader.load()

def load_ppt(path: str)->List[Document]:
    loader= UnstructuredPowerPointLoader(path)
    return loader.load()

def ocr_pdf(path: str) -> List[Document]:
    images=convert_from_path(path)
    texts=[]
    for i,im in enumerate(images):
        text=pytesseract.image_to_string(im)
        texts.append(Document(page_content=text, metadata={"page": i+1,"ocr":True}))

def load_document(uploaded_file):
    ext=uploaded_file.name.split('.')[-1].lower()
    with tempfile.NamedTemporaryFile(delete=False,suffix=f'.{ext}') as tmp:
        tmp.write(uploaded_file.read())
        path=tmp.name

    if ext == ".pdf":
        docs = load_pdf_pages(path)
        # fallback if no text
        if all(not d.page_content.strip() for d in docs):
            return ocr_pdf(path)
        return docs
    if ext in [".docx", ".doc"]:
        return load_docs(path)
    if ext in [".pptx", ".ppt"]:
        return load_ppt(path)
    raise ValueError("Unsupported file type")