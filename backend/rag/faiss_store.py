# backend/rag/faiss_store.py

from backend.config import FAISS_INDEX_PATH, FAISS_DOCS_PATH
import faiss
import pickle

class FAISSStore:
    def __init__(self, index_path: str, docs_path: str):
        self.index = faiss.read_index(index_path)
        with open(docs_path, "rb") as f:
            self.docs = pickle.load(f)

    def search(self, query: str, k: int = 3):
        # ⚠️ replace this with your real embedding logic
        return self.docs[:k]


# ✅ SINGLETON STORE (important)
_store = None


def get_faiss_store() -> FAISSStore:
    global _store
    if _store is None:
        _store = FAISSStore(
            index_path=FAISS_INDEX_PATH,
            docs_path=FAISS_DOCS_PATH,
        )
    return _store


# ✅ THIS is what you were missing
def search_faiss(query: str):
    store = get_faiss_store()
    return store.search(query)
