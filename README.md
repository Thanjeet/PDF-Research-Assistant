# 📄 PDF Research Assistant

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)  
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-green.svg)](https://streamlit.io/)  
[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)  

**Ask questions about your PDFs, get answers instantly!**  
A Streamlit-based AI assistant that reads your PDFs and responds to natural language queries using open-source embeddings and language models.

---

## 🚀 Features

- Upload single or multiple PDFs.  
- Chat with your documents—maintains conversation history.  
- Choose between **Flan-T5** or **Mistral** models.  
- Minimalist, interactive UI with chat bubbles.  
- Quick answers powered by vector embeddings.  

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
---
## ⚙️ Supported Models

| Model | Type | Notes |
|-------|------|-------|
| **Flan-T5 (HF)** | HuggingFace | Open-source text generation model |
| **Mistral (Ollama)** | Ollama | Must be pulled via `ollama pull mistral` |

---

## 📂 File Structure

PDF-Research-Assistant/
│
├─ app.py # Main Streamlit app
├─ requirements.txt # Python dependencies
├─ src/
│ ├─ loader.py # PDF loading & chunking
│ ├─ embeddings.py # Embeddings setup & retrieval
│ ├─ qa_engine.py # Question-answering logic
│ └─ utils.py # Helper functions
├─ config.yaml
└─ README.md

---


## 🧰 Dependencies

- **Streamlit** – Interactive web apps  
- **Sentence Transformers** – Text embeddings  
- **FAISS** – Fast vector search  
- **PyMuPDF / fitz** – PDF text extraction  

---

## 📈 Future Improvements
- Support for multiple PDFs
- Summarization mode
- Deploy on Hugging Face Spaces

---

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.

---
                     ┌─────────────────┐
                     │  app.py (UI)    │
                     │ - Streamlit UI  │
                     │ - Model select  │
                     │ - Chatbox       │
                     └─────┬───────────┘
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
┌───────────────┐                    ┌────────────────┐
│ loader.py     │                    │ embeddings.py  │
│ - pdf_to_chunks│◀── chunks ───────│ - build_embeddings │
│ - uses fitz    │                    │ - FAISS index     │
└───────────────┘                    │ - get_retriever  │
                                     └───────────────┘
                                            │
                                            ▼
                                     ┌───────────────┐
                                     │ qa_engine.py  │
                                     │ - ask_question│
                                     │ - uses retriever
                                     └───────────────┘
                                            │
                                            ▼
                                     ┌───────────────┐
                                     │ utils.py      │
                                     │ - chunk_text  │
                                     │ - preprocessing
                                     └───────────────┘

## Explanation

#### app.py
- Handles the Streamlit interface: uploading PDFs, selecting model, chat UI.
- Stores chat_history and retriever in session state.

#### loader.py
- Loads PDFs via PyMuPDF (fitz).
- Converts PDF text into chunks for embeddings.

#### embeddings.py
- Generates embeddings for text chunks using Sentence Transformers.
- Creates FAISS index for efficient similarity search.
- Provides get_retriever() to fetch top-k relevant chunks.

#### qa_engine.py
- Accepts a query and calls the retriever.
  Sends retrieved chunks to the selected model (Flan-T5 or Mistral) for answer generation.

#### utils.py
- Handles helper functions like text chunking, preprocessing, etc.
