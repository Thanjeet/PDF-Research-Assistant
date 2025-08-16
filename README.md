# 📄 PDF Research Assistant

An AI-powered tool that lets you **upload a PDF and ask questions about it**.  
It uses **embeddings + retrieval-based QA** to give accurate answers from the document.

---

## ⚡ Features
- Upload any PDF
- Embed document chunks using `sentence-transformers`
- Retrieve relevant sections with FAISS
- Answer questions using Hugging Face LLMs
- Simple **Streamlit UI**

---

## 🚀 Getting Started
### 1. Clone the repo
```bash
git clone https://github.com/thanjeet/pdf-research-assistant.git
cd pdf-research-assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```


