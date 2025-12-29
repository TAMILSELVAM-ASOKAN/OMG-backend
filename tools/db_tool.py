from utils.postgres_connector import get_db_connection
from langchain.tools import tool

def resolve_temple_fuzzy(temple_name: str, limit: int = 2):
    """
    Resolve temple using fuzzy matching directly on temples table.
    No alias table is used.
    
    Returns top matches with similarity scores and additional info.
    SQL Agent / LLM decides how to interpret results.
    """

    sql = """
    SELECT
    id,
    name,
    deity,
    city,
    state,
    timings,
    website,
    description,
    history,
    festivals,
    amenities,
    GREATEST(
        similarity(name, %(q)s),
        similarity(city, %(q)s),
        similarity(deity, %(q)s)
    ) AS score
    FROM temples
    WHERE
        similarity(name, %(q)s) > 0.3
        OR similarity(city, %(q)s) > 0.3
        OR similarity(deity, %(q)s) > 0.3
    ORDER BY score DESC
    LIMIT %(limit)s;
    """

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {"q": temple_name, "limit": limit})
            rows = cur.fetchall()

            if not rows:
                return []

            results = []
            for row in rows:
                results.append({
                    "temple_id": row[0],
                    "name": row[1],
                    "deity": row[2],
                    "city": row[3],
                    "state": row[4],
                    "timings": row[5],
                    "website": row[6],
                    "description": row[7],
                    "history": row[8],
                    "festivals": row[9],
                    "amenities": row[10],
                    "confidence": row[11]
                })

            return results

@tool
def temple_db_tool(temple_name: str) -> str:
    """Fetch verified temple details and timings from database."""
    return resolve_temple_fuzzy(temple_name)