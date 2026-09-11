from pydantic import ValidationError
import pytest
from app.models.users import UserCreate, UserUpdate, UserResponse


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