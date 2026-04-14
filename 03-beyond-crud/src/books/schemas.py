from pydantic import BaseModel

class Book(BaseModel):
    isbn10: str
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

class BookUpdate(BaseModel):
    title: str
    author: str
    page_count: int
    language: str
