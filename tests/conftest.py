import pytest
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection as Connection
from config import settings


# Replace with your real DB URL / params
DB_DSN = settings.DATABASE_URL


@pytest.fixture(scope="session")
def db_conn():
    """Session-scoped real DB connection."""
    conn = psycopg2.connect(DB_DSN, cursor_factory=RealDictCursor)
    conn.autocommit = False
    yield conn
    conn.close()


@pytest.fixture
def conn(db_conn):
    """
    Function-scoped connection that rolls back after each test,
    so your real data is never permanently modified.
    """
    yield db_conn
    db_conn.rollback()


@pytest.fixture
def seeded_user(conn):
    """Insert a throwaway user, return its row. Rolled back after test."""
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO users (username, email, password_hash, role, is_active)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, username, email, password_hash ,role, is_active, created_at, updated_at
            """,
            ("pytest_user", "pytest_user@example.com", "##HASH_EXAMPLE##", "admin", True),
        )
        user = cur.fetchone()
    return user