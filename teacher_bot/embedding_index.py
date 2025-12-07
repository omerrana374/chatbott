import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from .load_data import load_all_data

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_FILE = "faiss_index.bin"
META_FILE = "faiss_meta.npy"


def build_index():
    print("Loading model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Loading dataset...")
    dataset = load_all_data()
    print(f"Total records: {len(dataset)}")

    texts = []
    for item in dataset:
        if isinstance(item, dict):
            texts.append(item["text"])
        else:
            raise ValueError(
                "Detected non-dict item. Your JSONL loader must return dicts."
            )

    print("Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)
    embeddings = embeddings.astype("float32")

    dim = embeddings.shape[1]
    print(f"Embedding dimension: {dim}")

    print("Building FAISS index...")
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    print("Saving index...")
    faiss.write_index(index, INDEX_FILE)

    print("Saving metadata...")
    np.save(META_FILE, np.array(dataset, dtype=object))

    print("FAISS index successfully built!")
