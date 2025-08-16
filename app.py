import streamlit as st
from src.loader import load_pdf
from src.embeddings import embed_texts, create_vectorstore, get_retriever
from src.qa_engine import ask_question

st.title("📄 PDF Research Assistant")
st.write("Upload a PDF and ask questions about its content.")

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file:
    st.write("Processing PDF...")
    docs = load_pdf(uploaded_file)
    embeddings = embed_texts(docs)
    retriever = get_retriever(embeddings)

    query = st.text_input("Ask a question about the document:")
    if query:
        answer = ask_question(query, retriever)
        st.success(answer)
