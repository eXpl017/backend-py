from fastapi import FastAPI
from src.books.routes import book_router

version = 'v1'

app = FastAPI(
    title='PyBookApp',
    description='REST API for book application',
    version=version
)
app.include_router(book_router, prefix=f'/api/{version}/books', tags=['books'])
