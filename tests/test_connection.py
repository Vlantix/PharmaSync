import pytest

from db.connection import get_connection

def test_can_connect_to_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            assert cur.fetchone() is not None