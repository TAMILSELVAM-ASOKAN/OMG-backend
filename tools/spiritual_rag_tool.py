from langchain.tools import tool
from utils.vector_store import similarity_search


@tool
def spiritual_story_search(query: str) -> str:
    """
    Use this tool when the user asks about:
    - spiritual stories
    - god mythology
    - epics (Ramayana, Mahabharata, Bhagavatam)
    - legends, divine events
    """
    print("query",query)
    results = similarity_search(query)
    print("<><>",results)

    if not results:
        return "No relevant spiritual stories found."

    context_blocks = []
    for r in results:
        context_blocks.append(
            f"[Source: {r['source']} | Score: {round(r['score'], 2)}]\n{r['content']}"
        )

    return "\n\n".join(context_blocks)
