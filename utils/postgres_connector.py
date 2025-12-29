import os
import psycopg2
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

@contextmanager
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )
    try:
        yield conn
    finally:
        conn.close()
