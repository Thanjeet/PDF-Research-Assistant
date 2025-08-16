# src/utils.py
def chunk_text(text, chunk_size=500, chunk_overlap=50):
    """
    Split text into overlapping chunks
    """
    chunks = []
    start = 0
    text_length = len(text)
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - chunk_overlap
    return chunks
