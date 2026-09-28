from pydantic import ValidationError
import pytest
import psycopg2
from app.models.auth import LoginRequest, TokenResponse
from db.repository.auth import create_user, get_user_by_email, get_user_by_username


def test_login_request_valid():
    data = LoginRequest(username="kent", password="secret123")
    assert data.username == "kent"
    assert data.password == "secret123"

def test_login_request_missing_username():
    with pytest.raises(ValidationError):
        LoginRequest(password="secret123")

def test_login_request_missing_password():
    with pytest.raises(ValidationError):
        LoginRequest(username="kent")

def test_token_response_default_type():
    token = TokenResponse(access_token="abc123")
    assert token.token_type == "bearer"

def test_token_response_custom_type():
    token = TokenResponse(access_token="abc123", token_type="jwt")
    assert token.token_type == "jwt"

# ---------------------------------------------------------------------------
# get_user_by_username
# ---------------------------------------------------------------------------

def test_get_user_by_username_returns_user(conn, seeded_user):
    result = get_user_by_username(conn, "pytest_user")
    assert result is not None
    assert result["username"] == "pytest_user"
    assert result["id"] == seeded_user["id"]


def test_get_user_by_username_includes_password_hash(conn, seeded_user):
    """Login needs the hash — this is the only place it should be returned."""
    result = get_user_by_username(conn, "pytest_user")
    assert "password_hash" in result
    assert result["password_hash"] == seeded_user["password_hash"]


def test_get_user_by_username_returns_none_for_missing(conn):
    assert get_user_by_username(conn, "no_such_user") is None


def test_get_user_by_username_is_case_sensitive(conn, seeded_user):
    """Postgres string comparison is case-sensitive by default."""
    assert get_user_by_username(conn, "PYTEST_USER") is None


# ---------------------------------------------------------------------------
# get_user_by_email
# ---------------------------------------------------------------------------

def test_get_user_by_email_returns_user(conn, seeded_user):
    result = get_user_by_email(conn, "pytest_user@example.com")
    assert result is not None
    assert result["email"] == "pytest_user@example.com"
    assert result["id"] == seeded_user["id"]


def test_get_user_by_email_does_not_return_password_hash(conn, seeded_user):
    result = get_user_by_email(conn, "pytest_user@example.com")
    assert "password_hash" not in result


def test_get_user_by_email_returns_none_for_missing(conn):
    assert get_user_by_email(conn, "nobody@example.com") is None


# ---------------------------------------------------------------------------
# create_user
# ---------------------------------------------------------------------------

def test_create_user_returns_created_row(conn):
    result = create_user(
        conn,
        username="new_user",
        email="new_user@example.com",
        password_hash="hash_new",
        role="pharmacist",
    )
    assert result["username"] == "new_user"
    assert result["email"] == "new_user@example.com"
    assert result["role"] == "pharmacist"
    assert result["is_active"] is True
    assert "id" in result


def test_create_user_does_not_return_password_hash(conn):
    result = create_user(
        conn, "nohash", "nohash@example.com", "secret", "admin",
    )
    assert "password_hash" not in result


def test_create_user_persists_row(conn):
    created = create_user(
        conn, "persist", "persist@example.com", "h", "manager",
    )
    fetched = get_user_by_username(conn, "persist")
    assert fetched is not None
    assert fetched["id"] == created["id"]


def test_create_user_defaults_is_active_true(conn):
    result = create_user(
        conn, "active_default", "ad@example.com", "h", "admin",
    )
    assert result["is_active"] is True


def test_create_user_duplicate_username_raises(conn, seeded_user):
    with pytest.raises(psycopg2.errors.UniqueViolation):
        create_user(
            conn,
            username="pytest_user",
            email="other@example.com",
            password_hash="h",
            role="admin",
        )


def test_create_user_duplicate_email_raises(conn, seeded_user):
    with pytest.raises(psycopg2.errors.UniqueViolation):
        create_user(
            conn,
            username="other_name",
            email="pytest_user@example.com",
            password_hash="h",
            role="admin",
        )


def test_create_user_invalid_role_raises(conn):
    with pytest.raises(psycopg2.errors.CheckViolation):
        create_user(
            conn,
            username="bad_role",
            email="bad_role@example.com",
            password_hash="h",
            role="wizard",
        )