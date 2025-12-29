from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

@tool
def web_search_tool(query: str) -> str:
    """Search web for supplementary spiritual information."""
    tavily_tool = TavilySearchResults(max_results=5)
    results = tavily_tool.run(query)

    summarized = "\n".join(
        r["content"] for r in results[:3]
    )

    return summarized

