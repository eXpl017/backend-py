from uuid import UUID, uuid4
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import  SQLModel, Field, Column


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: UUID = Field(
        sa_column = Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            unique=True,
            default=uuid4
        )
    )
    isbn10: str
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
    published_date: str
    created_at: datetime = Field(
        sa_column = Column(
            pg.TIMESTAMP,
            default=datetime.now
        )
    )
    updated_at: datetime = Field(
        sa_column = Column(
            pg.TIMESTAMP,
            default=datetime.now
        )
    )

    def __repr__(self):
        return f"<Book {self.title}>"
