import PyPDF2
from src.utils import chunk_text

def load_pdf(file):
    """Extracts text from a PDF file and splits it into chunks."""
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    
    # Split into chunks for embeddings
    docs = chunk_text(text, chunk_size=500, overlap=50)
    return docs
