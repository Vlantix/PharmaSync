from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    """
    Request body for creating a new user.
    Used internally by POST /auth/register (Admin only).
    Role must be one of: 'admin', 'manager', 'pharmacist'.
    """
    username: str
    email: EmailStr
    password: str
    role: str

class UserUpdate(BaseModel):
    """
    Request body for PATCH /users/{user_id}.
    All fields are optional — only provided fields will be updated.
    """
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    """
    Safe user representation.
    Never exposes password_hash or sensitive fields.
    """
    id: int
    username: str
    email: str
    role: str
    is_active: bool

    