from tavily import TavilyClient
from backend.config import TAVILY_API_KEY

client = TavilyClient(api_key=TAVILY_API_KEY)

def tavily_search(query: str) -> str:
    result = client.search(
        query=query,
        max_results=5,
        include_answer=True
    )

    if not result or "results" not in result:
        return "NO_CONTEXT"

    return "\n".join(r["content"] for r in result["results"])
