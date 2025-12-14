import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from .load_data import load_all_data
from .doc_loader import load_all_docs

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_FILE = "faiss_index.bin"
META_FILE = "faiss_meta.npy"


def build_index():
    print("Loading model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Loading synthetic dataset...")
    dataset = load_all_data()
    print(f"Synthetic dataset records: {len(dataset)}")

    print("Loading documentation...")
    docs = load_all_docs()
    print(f"Documentation records: {len(docs)}")

    full_data = dataset + docs
    print(f"Total combined records: {len(full_data)}")

    texts = [item["text"] for item in full_data]

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
    np.save(META_FILE, np.array(full_data, dtype=object))

    print("FAISS index successfully built!")
