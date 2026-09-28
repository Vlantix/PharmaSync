from typing import Optional
from psycopg2.extensions import connection as Connection

def get_user_by_username(conn: Connection, username: str) -> Optional[dict]:
    """
    Fetch a single user by username.
    Used during login to verify credentials.
    Returns None if user not found.
    """
    with conn.cursor() as curs:
        curs.execute("""
        SELECT id, username, email, password_hash, role, is_active
        FROM users
        WHERE username = %s
        """, (username,))
        row = curs.fetchone()
        return dict(row) if row else None

def get_user_by_email(conn: Connection, email: str) -> Optional[dict]:
    """
    Fetch a single user by email.
    Used to check for duplicate emails during registration.
    Returns None if user not found.
    """
    with conn.cursor() as curs:
        curs.execute("""
        SELECT id, username, email, role, is_active
        FROM users
        WHERE email = %s
        """, (email,))
        row = curs.fetchone()
        return dict(row) if row else None

def create_user(
        conn: Connection,
        username: str,
        email: str,
        password_hash: str,
        role: str
    ) -> dict:
    """
    Insert a new user into the database.
    Returns the created user record.
    Used by: POST /auth/register.
    """
    with conn.cursor() as curs:
        curs.execute("""
        INSERT INTO users(username, email, password_hash, role)
        VALUES (%s, %s, %s, %s)
        RETURNING id, username, email, role, is_active
        """, (username, email, password_hash, role,))
        row = curs.fetchone()
        return dict(row)
