from backend.rag.faiss_store import FAISSStore
from backend.config import FAISS_INDEX_PATH, FAISS_DOCS_PATH

# Example knowledge — replace with your real data
documents = [
    "Blismos Academy teaches Generative AI",
    "We offer LLM, RAG, and Agent courses",
    "FAISS is used for semantic search",
]

store = FAISSStore(
    index_path=FAISS_INDEX_PATH,
    docs_path=FAISS_DOCS_PATH,
)

store.build(documents)

print("✅ FAISS index built successfully")
