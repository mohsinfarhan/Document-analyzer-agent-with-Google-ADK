import faiss
import numpy as np

class VectorStore:
    def __init__(self, dimension: int):
        self.index = faiss.IndexFlatL2(dimension)
        self.chunks = []

    def add_to_index(self, chunks: list[str], embeddings: np.ndarray):
        self.chunks.extend(chunks)
        self.index.add(embeddings)

    def search(self, query_embedding: np.ndarray, k: int = 3):
        distances, indices = self.index.search(query_embedding, k)
        return [self.chunks[i] for i in indices[0] if i != -1]