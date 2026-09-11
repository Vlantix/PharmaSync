from pydantic import BaseModel
from app.models.users import UserCreate, UserResponse

class LoginRequest(BaseModel):
    """
    Request body for POST /auth/login.
    Used by all roles to authenticate and receive a JWT token.
    """
    username: str
    password: str

class TokenResponse(BaseModel):
    """
    Response for POST /auth/login.
    Returns a JWT bearer token used for authenticating subsequent requests.
    """
    access_token: str
    token_type: str = "bearer"
