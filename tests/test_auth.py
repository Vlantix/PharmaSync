from pydantic import ValidationError
import pytest
from app.models.auth import LoginRequest, TokenResponse


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