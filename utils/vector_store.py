from langchain_openai import OpenAIEmbeddings
from utils.postgres_connector import get_db_connection

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")


def store_documents(texts: list[str], source: str):
    embeddings = embedding_model.embed_documents(texts)

    sql = """
    INSERT INTO spiritual_documents (source, content, embedding)
    VALUES (%s, %s, %s)
    """

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            for text, emb in zip(texts, embeddings):
                cur.execute(sql, (source, text, emb))
        conn.commit()


def similarity_search(query: str, limit: int = 4):
    print("QUERY><>",query)
    query_embedding = embedding_model.embed_query(query)

    sql = """
    SELECT
        content,
        source,
        1 - (embedding <=> %s::vector) AS score
    FROM spiritual_documents
    ORDER BY embedding <=> %s::vector
    LIMIT %s;
    """
    print("SQL><>",sql)
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql,
                (
                    query_embedding,
                    query_embedding,
                    limit
                )
            )
            rows = cur.fetchall()

    return [
        {
            "content": r[0],
            "source": r[1],
            "score": float(r[2])
        }
        for r in rows
    ]

