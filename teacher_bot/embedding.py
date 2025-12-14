import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_model = None


def load_embed_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed_text(text: str):
    model = load_embed_model()
    emb = model.encode([text], convert_to_numpy=True)
    return emb.astype("float32")[0]
