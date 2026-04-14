from fastapi import APIRouter, Header, status
from fastapi.exceptions import HTTPException
from .books_data import books
from .schemas import Book, BookUpdate

##### Router Object

book_router = APIRouter()

##### Routes

@book_router.get('/get_headers')
async def get_headers(
    accept: str = None
) -> dict:
    pass

@book_router.get('/books', response_model=list[Book])
async def get_all_books():
    return books

@book_router.post('/books', status_code=status.HTTP_201_CREATED)
async def create_book(book_data: Book) -> dict:
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book

@book_router.get('/book/{book_isbn}')
async def get_book(book_isbn: str) -> dict:
    for book in books:
        if book.get('isbn10', None) == book_isbn:
            return book
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested resource could not be found."
        )

@book_router.patch('/book/{book_isbn}')
async def update_book(book_isbn: str, book_update: BookUpdate) -> dict:
    for book in books:
        if book.get('isbn10', None)==book_isbn:
            book.update(
                {
                    'title': book_update.title,
                    'author': book_update.author,
                    'page_count': book_update.page_count,
                    'language': book_update.language
                }
            )

            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Book not found'
    )

@book_router.delete('/book/{book_isbn}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_isbn: str):
    for book in books:
        if book.get('isbn10', None) == book_isbn:
            books.remove(book)

            return {}
