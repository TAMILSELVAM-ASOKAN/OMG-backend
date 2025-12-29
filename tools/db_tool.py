from utils.postgres_connector import get_db_connection


def resolve_temple_fuzzy(temple_name: str, limit: int = 1):
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
        similarity(name, %(q)s) ::float AS confidence
    FROM temples
    ORDER BY confidence DESC
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
