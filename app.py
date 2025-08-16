# app.py
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
from src.loader import pdf_to_chunks
from src.vectorstore import build_embeddings, get_retriever
from src.qa_engine import ask_question

# ---- Model Configurations ----
model_configs = {
    "Flan-T5 (HF)": {
        "backend": "huggingface",
        "model": "google/flan-t5-small",
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    },
    "Mistral (Ollama)": {
        "backend": "ollama",
        "model": "mistral",
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    },
}

# ---- Streamlit Setup ----
st.set_page_config(page_title="PDF Research Assistant", layout="wide")
st.title("📄 PDF Research Assistant")

# ---- Sidebar ----
st.sidebar.header("⚙️ Settings")
selected_model_name = st.sidebar.selectbox("Choose a model", list(model_configs.keys()))
model_config = model_configs[selected_model_name]

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF(s)", type=["pdf"], accept_multiple_files=True
)

if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.chat_history = []
    st.sidebar.success("Chat history cleared!")

# ---- Initialize session state ----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "retriever" not in st.session_state and uploaded_files:
    all_chunks = []
    for pdf in uploaded_files:
        chunks = pdf_to_chunks(pdf)
        all_chunks.extend(chunks)
    embeddings_store = build_embeddings(all_chunks, model_config["embedding_model"])
    st.session_state.retriever = get_retriever(embeddings_store)
    st.session_state.embeddings_store = embeddings_store

# ---- Chat UI ----
st.subheader(f"💬 Chat with {selected_model_name}")

# Custom CSS for chat bubbles
st.markdown("""
<style>
.chat-container {
    max-height: 500px;
    overflow-y: auto;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 12px;
    background-color: #f9f9f9;
}
.user-bubble {
    background-color: #DCF8C6;
    padding: 10px 14px;
    border-radius: 16px;
    margin: 6px 0;
    max-width: 80%;
    float: right;
    clear: both;
}
.assistant-bubble {
    background-color: #E9E9EB;
    padding: 10px 14px;
    border-radius: 16px;
    margin: 6px 0;
    max-width: 80%;
    float: left;
    clear: both;
}
</style>
""", unsafe_allow_html=True)

# Display chat history
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for chat in st.session_state.chat_history:
    role = chat["role"]
    content = chat["content"]
    if role == "user":
        st.markdown(f"<div class='user-bubble'>🧑 {content}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='assistant-bubble'>🤖 {content}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---- Chat Input ----
with st.form(key="chat_form", clear_on_submit=True):
    query = st.text_area("💬 Type your message:", height=80)
    submit = st.form_submit_button("Send")

if submit and query.strip():
    st.session_state.chat_history.append({"role": "user", "content": query})
    with st.spinner("🤔 Thinking..."):
        answer = ask_question(query, st.session_state.retriever, model_config)
    st.session_state.chat_history.append({"role": "assistant", "content": answer})
