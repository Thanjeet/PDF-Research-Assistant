# src/qa_engine.py
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# Load a small model once for inference
MODEL_CACHE = {}

def load_model(model_name="google/flan-t5-small"):
    if model_name in MODEL_CACHE:
        return MODEL_CACHE[model_name]
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    MODEL_CACHE[model_name] = (tokenizer, model)
    return tokenizer, model

def ask_question(question, retriever, model_config):
    """
    Retrieve context from PDFs and generate answer
    """
    # Retrieve top chunks
    context_chunks = retriever(question)
    context = " ".join(context_chunks)

    # Load model
    tokenizer, model = load_model(model_config["model"])

    input_text = f"question: {question} context: {context}"
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512)

    # Generate
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=200)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer
