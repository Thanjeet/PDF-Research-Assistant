# src/loader.py
import fitz  # PyMuPDF
from src.utils import chunk_text

def pdf_to_chunks(file, chunk_size=500, chunk_overlap=50):
    """
    Extract text from PDF and split into chunks
    """
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    chunks = chunk_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return chunks
