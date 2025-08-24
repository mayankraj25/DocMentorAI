import streamlit as st
from dotenv import load_dotenv
from backend.ingestion import ingest_documents
from backend.query_engine import query_documents
from utils.summarizer import summarize_text

load_dotenv()

st.set_page_config(page_title="📚 DocuMentorAI", layout="wide")
st.title("📚 DocuMentorAI - Your Smart Document Assistant")

uploaded_files = st.file_uploader("Upload PDF, DOCX, or TXT files", type=["pdf", "docx", "txt"], accept_multiple_files=True)

# Store vectordb in session state
if "vectordb" not in st.session_state:
    st.session_state.vectordb = None

if uploaded_files and st.button("Process Documents"):
    with st.spinner("🔍 Processing documents..."):
        vectordb,raw_text = ingest_documents(uploaded_files)
        st.session_state.vectordb = vectordb
        st.session_state.raw_text = raw_text
    st.success("✅ Documents processed successfully.")

if st.session_state.vectordb:
    if st.button("Summarize Documents"):
        with st.spinner("📝 Summarizing documents..."):
            summaries = summarize_text(st.session_state.raw_text)
        st.write("**Summaries:**")
        st.write(summaries)

    query = st.text_input("Ask a question about the documents:")
    if query:
        with st.spinner("🤖 Generating answer..."):
            result = query_documents(query, st.session_state.vectordb)
        st.write("**Answer:**", result)