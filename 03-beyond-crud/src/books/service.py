from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreate, BookUpdate
from .models import Book


class BookService:
    def __init__(self):
        pass

    async def get_all_books(self, session: AsyncSession):
        stmt = select(Book).order_by(desc(Book.created_at))
        res = await session.exec(stmt)
        return res.all()

    async def get_book(self, book_uid: str, session: AsyncSession):
        stmt = select(Book).where(Book.uid==book_uid)
        res = await session.exec(stmt)
        return res.first() if res else None

    async def create_book(self, book_data: BookCreate, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)
        session.add(new_book)
        await session.commit()
        return new_book

    async def update_book(self, book_uid:str, update_data: BookUpdate, session: AsyncSession):
        book_to_update = await self.get_book(book_uid, session)
        if not book_to_update:
            print(f'Book with UID not found')
            return None

        update_data_dict = update_data.model_dump()
        for k,v in update_data_dict.items():
            if v:
                setattr(book_to_update, k, v)

        await session.commit()
        return book_to_update

    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)
        if not book_to_delete:
            print(f'Book with UID not found')
            return None

        await session.delete(book_to_delete)
        await session.commit()
        return {}
