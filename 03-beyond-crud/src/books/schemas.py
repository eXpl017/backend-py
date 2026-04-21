from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class Book(BaseModel):
    uid: UUID
    isbn10: str
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
    published_date: str
    created_at: datetime
    updated_at: datetime


class BookCreate(BaseModel):
    isbn10: str
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
    published_date: str


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    page_count: int | None = None
    language: str | None = None
