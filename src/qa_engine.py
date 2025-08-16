from transformers import pipeline

# Load Hugging Face QA pipeline (small model for free usage)
_qa_model = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

def ask_question(query, retriever):
    """
    Retrieve relevant chunks and run QA pipeline.
    If QA model fails, fallback to returning top retrieved chunks.
    """
    relevant_chunks = retriever(query)
    combined_context = " ".join(relevant_chunks)

    if not combined_context.strip():
        return "I couldn't find relevant information in the document."

    try:
        result = _qa_model(question=query, context=combined_context)
        return result["answer"]
    except Exception:
        # Fallback if the model crashes
        return f"Top relevant context: {relevant_chunks[0]}"
