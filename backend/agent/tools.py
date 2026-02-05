from agents.tool import FunctionTool
from backend.rag.faiss_store import FAISSStore
from tavily import TavilyClient
from backend.config import FAISS_INDEX_PATH, FAISS_DOCS_PATH, TAVILY_API_KEY

# -------- singletons --------
_faiss_store = None
_tavily_client = None


def get_faiss_store():
    global _faiss_store
    if _faiss_store is None:
        _faiss_store = FAISSStore(
            index_path=FAISS_INDEX_PATH,
            docs_path=FAISS_DOCS_PATH,
        )
    return _faiss_store


def get_tavily_client():
    global _tavily_client
    if _tavily_client is None:
        _tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    return _tavily_client


# -------- tool logic --------

def search_academy_knowledge(query: str) -> str:
    store = get_faiss_store()
    results = store.search(query)
    return "\n".join(results) if results else "No academy data found."


def web_search(query: str) -> str:
    tavily = get_tavily_client()
    res = tavily.search(query=query, max_results=3)
    return "\n".join(r["content"] for r in res.get("results", []))


# -------- REQUIRED schemas --------

academy_schema = {
    "type": "object",
    "properties": {
        "query": {"type": "string"},
    },
    "required": ["query"],
}

# -------- TOOL OBJECTS (THIS FIXES EVERYTHING) --------

academy_search_tool = FunctionTool(
    name="search_academy_knowledge",
    description="Search Blismos Academy internal FAISS knowledge base",
    params_json_schema=academy_schema,
    on_invoke_tool=lambda args: search_academy_knowledge(args["query"]),
)

web_search_tool = FunctionTool(
    name="web_search",
    description="Search the web using Tavily",
    params_json_schema=academy_schema,
    on_invoke_tool=lambda args: web_search(args["query"]),
)
