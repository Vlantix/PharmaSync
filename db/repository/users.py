from typing import Optional
from psycopg2.extensions import connection as Connection


def get_all_users(conn: Connection) -> list[dict]:
    """
    Fetch all users.
    Used by GET /users (Admin only).
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, username, email, role, is_active, created_at, updated_at
            FROM users
            ORDER BY created_at DESC
            """
        )
        return [dict(row) for row in cur.fetchall()]


def get_user_by_id(conn: Connection, user_id: int) -> Optional[dict]:
    """
    Fetch a single user by ID.
    Used by PATCH /users/{user_id} and DELETE /users/{user_id}.
    Returns None if not found.
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, username, email, role, is_active, created_at, updated_at
            FROM users
            WHERE id = %s
            """,
            (user_id,)
        )
        row = cur.fetchone()
        return dict(row) if row else None


def update_user(
    conn: Connection,
    user_id: int,
    username: Optional[str] = None,
    email: Optional[str] = None,
    role: Optional[str] = None,
    is_active: Optional[bool] = None
) -> Optional[dict]:
    """
    Partially update a user using COALESCE.
    Only updates fields that are not None.
    Used by PATCH /users/{user_id} (Admin only).
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE users SET
                username = COALESCE(%s, username),
                email = COALESCE(%s, email),
                role = COALESCE(%s, role),
                is_active = COALESCE(%s, is_active),
                updated_at = clock_timestamp()
            WHERE id = %s
            RETURNING id, username, email, role, is_active, created_at, updated_at
            """,
            (username, email, role, is_active, user_id)
        )
        row = cur.fetchone()
        return dict(row) if row else None


def deactivate_user(conn: Connection, user_id: int) -> Optional[dict]:
    """
    Soft delete a user by setting is_active to FALSE.
    Used by DELETE /users/{user_id} (Admin only).
    Returns updated user or None if not found.
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE users
            SET is_active = FALSE, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING id, username, email, role, is_active
            """,
            (user_id,)
        )
        row = cur.fetchone()
        return dict(row) if row else None