from pydantic import ValidationError
import pytest
import time
from app.models.users import UserCreate, UserUpdate, UserResponse
from db.repository.users import (
    get_all_users,
    get_user_by_id,
    update_user,
    deactivate_user,
)


def test_user_create_valid():
    user = UserCreate(username="kent", email="kent@email.com", password="pass123", role="admin")
    assert user.username == "kent"
    assert user.role == "admin"

def test_user_create_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(username="kent", email="notanemail", password="pass123", role="admin")

def test_user_create_missing_fields():
    with pytest.raises(ValidationError):
        UserCreate(username="kent")

def test_user_update_all_optional():
    update = UserUpdate()
    assert update.username is None
    assert update.email is None
    assert update.role is None
    assert update.is_active is None

def test_user_update_partial():
    update = UserUpdate(role="pharmacist", is_active=False)
    assert update.role == "pharmacist"
    assert update.is_active is False

def test_user_response_valid():
    user = UserResponse(id=1, username="kent", email="kent@email.com", role="admin", is_active=True)
    assert user.id == 1
    assert user.is_active is True

# ---------------------------------------------------------------------------
# get_all_users
# ---------------------------------------------------------------------------

def test_get_all_users_returns_list_of_dicts(conn, seeded_user):
    result = get_all_users(conn)
    assert isinstance(result, list)
    assert all(isinstance(r, dict) for r in result)
    assert any(r["id"] == seeded_user["id"] for r in result)


def test_get_all_users_ordered_by_created_at_desc(conn, seeded_user):
    result = get_all_users(conn)
    timestamps = [r["created_at"] for r in result]
    assert timestamps == sorted(timestamps, reverse=True)


# ---------------------------------------------------------------------------
# get_user_by_id
# ---------------------------------------------------------------------------

def test_get_user_by_id_returns_seeded_user(conn, seeded_user):
    result = get_user_by_id(conn, seeded_user["id"])
    assert result is not None
    assert result["id"] == seeded_user["id"]
    assert result["username"] == "pytest_user"


def test_get_user_by_id_returns_none_for_missing(conn):
    assert get_user_by_id(conn, -1) is None


# ---------------------------------------------------------------------------
# update_user
# ---------------------------------------------------------------------------

def test_update_user_username_only(conn, seeded_user):
    result = update_user(conn, seeded_user["id"], username="renamed")
    assert result["username"] == "renamed"
    assert result["email"] == "pytest_user@example.com"


def test_update_user_email_only(conn, seeded_user):
    result = update_user(conn, seeded_user["id"], email="new@example.com")
    assert result["email"] == "new@example.com"
    assert result["username"] == "pytest_user"


def test_update_user_role(conn, seeded_user):
    result = update_user(conn, seeded_user["id"], role="admin")
    assert result["role"] == "admin"


def test_update_user_is_active(conn, seeded_user):
    result = update_user(conn, seeded_user["id"], is_active=False)
    assert result["is_active"] is False


def test_update_user_multiple_fields(conn, seeded_user):
    result = update_user(
        conn, seeded_user["id"],
        username="multi", email="multi@example.com", role="admin",
    )
    assert result["username"] == "multi"
    assert result["email"] == "multi@example.com"
    assert result["role"] == "admin"


def test_update_user_changes_updated_at(conn, seeded_user):
    before = seeded_user["updated_at"]
    result = update_user(conn, seeded_user["id"], username="ts_check")
    assert result["updated_at"] > before


def test_update_user_returns_none_for_missing(conn):
    assert update_user(conn, -1, username="ghost") is None


def test_update_user_no_args_leaves_row_unchanged(conn, seeded_user):
    result = update_user(conn, seeded_user["id"])
    assert result["username"] == seeded_user["username"]
    assert result["email"] == seeded_user["email"]


# ---------------------------------------------------------------------------
# deactivate_user
# ---------------------------------------------------------------------------

def test_deactivate_user_sets_is_active_false(conn, seeded_user):
    result = deactivate_user(conn, seeded_user["id"])
    assert result["is_active"] is False
    assert result["id"] == seeded_user["id"]


def test_deactivate_user_keeps_row(conn, seeded_user):
    deactivate_user(conn, seeded_user["id"])
    still_there = get_user_by_id(conn, seeded_user["id"])
    assert still_there is not None
    assert still_there["is_active"] is False


def test_deactivate_user_returns_none_for_missing(conn):
    assert deactivate_user(conn, -1) is None


def test_deactivate_user_twice_is_idempotent(conn, seeded_user):
    first = deactivate_user(conn, seeded_user["id"])
    second = deactivate_user(conn, seeded_user["id"])
    assert first["is_active"] is False
    assert second["is_active"] is False