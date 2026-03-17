from sentence_transformers import SentenceTransformer
import numpy as np

class Embedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # This will download the model (approx 90MB) on first run
        self.model = SentenceTransformer(model_name)

    def get_embeddings(self, text_chunks: list[str]) -> np.ndarray:
        """Converts text chunks into a float32 numpy array for FAISS."""
        embeddings = self.model.encode(text_chunks)
        return np.array(embeddings).astype("float32")