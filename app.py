import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE=os.get_env("API_BASE","http://localhost:8000")
st.set_page_config(page_title="Chat with Documents", layout="wide")
st.title("📄 Chat with Your Document")

if "token" not in st.session_state:
    st.session_state.token=None

with st.expander("Account (Optional)"):
    col1,col2=st.columns(2)
    with col1:
        reg_user=st.text_input("Register username")
        reg_password=st.text_input("Register password", type="password")
        if st.button("Register"):
            r=requests.post(f"{API_BASE}/register",json={"username":reg_user,"password":reg_password})
            st.write(r.json())
    with col2:
        login_user=st.text_input("Login username")
        login_pass=st.text_input("Login password")
        if st.button("Login"):
            r=requests.post(f"{API_BASE}/login",json={"username":login_user,"password":login_pass})
            if r.status_code==200:
                st.session_state.token=r.json()["access_token"]
                st.success("Logged in")
            else:
                st.error(r.json())



# if "chat_chain" not in st.session_state:
#     st.session_state.chat_chain = None
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "pptx"])
# if uploaded_file and st.button("Process Document"):
#     with st.spinner("Processing document..."):
#         document = load_document(uploaded_file)
#         vectordb = build_vectorstore(document)
#         st.session_state.chat_chain = create_chatchain(vectordb)
#         st.session_state.messages = []
#         st.success("Document processed and vector store created.")

# if st.session_state.chat_chain:
#     # Display chat history
#     for msg in st.session_state.messages:
#         if msg["role"] == "user":
#             with st.chat_message("user"):
#                 st.markdown(msg["content"])
#         else:
#             with st.chat_message("assistant"):
#                 st.markdown(msg["content"])

#     # Chat input (automatically clears after submit)
#     user_input = st.chat_input("Ask something about your document...")
#     if user_input:
#         st.session_state.messages.append({"role": "user", "content": user_input})
#         with st.chat_message("assistant"):
#             with st.spinner("Thinking..."):
#                 response = st.session_state.chat_chain({"question": user_input})
#             bot_reply = response["answer"]
#             st.markdown(bot_reply)
#         st.session_state.messages.append({"role": "assistant", "content": bot_reply})