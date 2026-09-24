import psycopg2
import psycopg2.extras
from contextlib import contextmanager
from config import settings

@contextmanager
def get_connection():
    conn = psycopg2.connect(
        settings.DATABASE_URL,
        cursor_factory=psycopg2.extras.DictCursor
    )

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def get_db():
    with get_connection() as conn:
        yield conn
