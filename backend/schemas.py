from pydantic import BaseModel
from typing import Optional

# Schema for creating a sweet
class SweetCreate(BaseModel):
    name: str
    category: str
    price: float
    quantity: int

# Schema for returning sweet info
class SweetResponse(BaseModel):
    id: int
    name: str
    category: str
    price: float
    quantity: int

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool = False

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
