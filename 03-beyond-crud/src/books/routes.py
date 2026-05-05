from fastapi import APIRouter, Header, status, Depends
from fastapi.exceptions import HTTPException
from .schemas import Book, BookCreate, BookUpdate
from src.books.service import BookService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import AccessTokenBearer


##### Router Object

book_router = APIRouter(prefix='/books')
book_service = BookService()
access_token_bearer = AccessTokenBearer()

##### Routes

@book_router.get('/get_headers')
async def get_headers(
    accept: str = None
) -> dict:
    pass


@book_router.get('/', response_model=list[Book])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    user_details = Depends(access_token_bearer)
):
    books = await book_service.get_all_books(session)
    return books


@book_router.post('/', status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(
    book_data: BookCreate,
    session: AsyncSession = Depends(get_session),
    user_details = Depends(access_token_bearer)
) -> dict:
    new_book = await book_service.create_book(book_data, session)
    return new_book


@book_router.get('/{book_uid}', response_model=Book)
async def get_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    user_details = Depends(access_token_bearer)
) -> dict:
    book = await book_service.get_book(book_uid, session)
    if not book:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Fetch failed. Book not found'
        )
    return book


@book_router.patch('/{book_uid}', response_model=Book)
async def update_book(
    book_uid: str,
    book_update: BookUpdate,
    session: AsyncSession = Depends(get_session),
    user_details = Depends(access_token_bearer)
) -> dict:
    updated_book = await book_service.update_book(book_uid, book_update, session)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Patch Failed. Book not found'
        )
    return updated_book


@book_router.delete('/{book_uid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    user_details = Depends(access_token_bearer)
):
    book_delete = await book_service.delete_book(book_uid, session)
    if book_delete is None:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Delete Failed. Book not found'
        )
    return {}
