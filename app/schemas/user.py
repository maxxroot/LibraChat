# app/schemas/user.py

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str | None = None
    is_active: bool = True

class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    domain: str

    class Config:
        from_attributes = True
