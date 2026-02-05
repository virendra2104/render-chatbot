from sentence_transformers import SentenceTransformer
import numpy as np

# Local embedding model (no API, no key)
_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts: list[str]) -> np.ndarray:
    """
    Generate vector embeddings locally for FAISS.
    """
    return _model.encode(texts, convert_to_numpy=True)
