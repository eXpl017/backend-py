from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def lifespan(app:FastAPI):
    print('Server started...')
    await init_db()
    yield
    print('Server stopped...')


version = 'v1'

app = FastAPI(
    title='PyBookApp',
    description='REST API for book application',
    version=version,
    lifespan=lifespan
)
app.include_router(book_router, prefix=f'/api/{version}/books', tags=['books'])
