from langchain_community.document_loaders import PyPDFLoader

def load_pdf_docs(path):
    loader= PyPDFLoader(path)
    return loader.load()

