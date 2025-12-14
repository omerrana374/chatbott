import os
import faiss
import numpy as np

from .embedding import embed_text

INDEX_FILE = "faiss_index.bin"
META_FILE = "faiss_meta.npy"


def load_index():
    if not os.path.exists(INDEX_FILE):
        raise FileNotFoundError("FAISS index not found. Build it first.")
    return faiss.read_index(INDEX_FILE)


def load_metadata():
    if not os.path.exists(META_FILE):
        return []
    arr = np.load(META_FILE, allow_pickle=True)
    return list(arr)


def save_index(index):
    faiss.write_index(index, INDEX_FILE)


def save_metadata(meta):
    np.save(META_FILE, np.array(meta, dtype=object))


def add_to_index(text: str, source: str = "doc"):
    """
    Embeds the new text and appends it to FAISS index and metadata.
    """
    emb = embed_text(text)

    index = load_index()
    meta = load_metadata()

    index.add(np.array([emb], dtype="float32"))
    meta.append({"text": text, "solution": None, "source": source})

    save_index(index)
    save_metadata(meta)
