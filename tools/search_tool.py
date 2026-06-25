from tavily import TavilyClient
from langchain.tools import tool
import os

@tool
def search_news(query: str) -> str:
    """Search the web for news articles related to a claim."""
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    results = client.search(query=query, max_results=5)
    summaries = [
        f"- {r['title']}: {r['content'][:200]}"
        for r in results['results']
    ]
    return "\n".join(summaries)