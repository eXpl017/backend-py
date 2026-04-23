from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class User(BaseModel):
    uid: UUID
    username: str
    email: str
    firstname: str
    lastname: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseModel):
    username: str = Field(max_length=8)
    firstname: str = Field(max_length=25)
    lastname: str = Field(max_length=25)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
