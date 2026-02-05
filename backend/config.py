import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "development")
DEBUG = ENV == "development"

# LLM
MODEL_NAME = "litellm/openrouter/mistralai/mistral-7b-instruct"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Tokens & Memory
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 512))
MEMORY_WINDOW_SIZE = int(os.getenv("MEMORY_WINDOW_SIZE", 6))

# Sessions
SESSION_TTL_SECONDS = int(os.getenv("SESSION_TTL_SECONDS", 3600))

# Security
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = int(
    os.getenv("JWT_EXPIRATION_SECONDS", 3600)
)

# Rate limiting
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", 60))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", 60))

# Cache / Redis
REDIS_URL = os.getenv("REDIS_URL")  # optional
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true") == "true"
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", 300))

# RAG
VECTOR_DB_PROVIDER = os.getenv("VECTOR_DB_PROVIDER", "faiss")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/vector_store")

# Telemetry / Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
ENABLE_TELEMETRY = os.getenv("ENABLE_TELEMETRY", "true") == "true"

# Streaming
ENABLE_STREAMING = True

# External tools
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

CHROMA_PERSIST_DIR = "./chroma_db"
FAISS_INDEX_PATH = "backend/data/faiss.index"
FAISS_DOCS_PATH = "backend/data/docs.pkl"
