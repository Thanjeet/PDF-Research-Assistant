# src/vectorstore.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, embedding_model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(embedding_model_name)
        self.index = None
        self.chunks = []

    def build(self, chunks):
        """
        Build FAISS index from text chunks
        """
        self.chunks = chunks
        vectors = self.model.encode(chunks, convert_to_numpy=True)
        dim = vectors.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(vectors)
        return self

    def get_retriever(self, top_k=3):
        """
        Return a retriever function
        """
        def retrieve(query):
            if self.index is None:
                raise ValueError("Embeddings not built yet.")
            q_vec = self.model.encode([query], convert_to_numpy=True)
            D, I = self.index.search(q_vec, top_k)
            results = [self.chunks[i] for i in I[0]]
            return results
        return retrieve

# Helper functions
def build_embeddings(chunks, embedding_model_name):
    store = VectorStore(embedding_model_name)
    return store.build(chunks)

def get_retriever(store, top_k=3):
    return store.get_retriever(top_k)
