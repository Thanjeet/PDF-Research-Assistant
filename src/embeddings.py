from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load once globally (efficient)
_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts):
    """Generate embeddings for a list of texts."""
    embeddings = _model.encode(texts, convert_to_numpy=True)
    return embeddings

def create_vectorstore(texts, embeddings):
    """Create a FAISS index from embeddings and store mapping to texts."""
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return {"index": index, "texts": texts}

def get_retriever(embeddings_store, top_k=3):
    """Return a retriever function that fetches top_k similar chunks."""
    def retrieve(query):
        query_vec = _model.encode([query], convert_to_numpy=True)
        D, I = embeddings_store["index"].search(query_vec, top_k)
        return [embeddings_store["texts"][i] for i in I[0]]
    return retrieve
