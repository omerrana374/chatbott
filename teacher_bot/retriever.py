import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_FILE = "faiss_index.bin"
META_FILE = "faiss_meta.npy"


class Retriever:
    def __init__(self):
        print("Loading model...")
        self.model = SentenceTransformer(MODEL_NAME)

        print("Loading FAISS index...")
        self.index = faiss.read_index(INDEX_FILE)

        print("Loading metadata...")
        self.metadata = np.load(META_FILE, allow_pickle=True)

        print("Retriever ready!")

    def search(self, query, top_k=5):
        query_emb = self.model.encode([query], convert_to_numpy=True).astype("float32")
        distances, indices = self.index.search(query_emb, top_k)

        results = []

        for dist, idx in zip(distances[0], indices[0]):
            item = self.metadata[idx]

            solution = None

            if "solution" in item:
                solution = item["solution"]

            elif "output" in item and "Solution" in item["output"]:
                solution = item["output"]["Solution"]

            else:
                solution = "No solution available"

            results.append(
                {
                    "text": item.get("text") or item.get("instruction") or "unknown",
                    "solution": solution,
                    "source": item.get("source", "unknown"),
                    "distance": float(dist),
                }
            )

        return results


if __name__ == "__main__":
    r = Retriever()
    results = r.search("What is mitosis?", top_k=3)
    for r_ in results:
        print(r_)
