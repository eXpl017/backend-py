from .models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .schemas import UserCreate
from .utils import hash_passwd

class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        stmt = select(User).where(User.email==email)
        res = await session.exec(stmt)
        user = res.first()
        return user

    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)
        return True if user is not None else False

    async def create_user(self, user_data: UserCreate, session: AsyncSession) -> User:
        user_data_dict = user_data.model_dump()
        hashed_passwd = hash_passwd(user_data_dict['password'])
        new_user = User(**user_data_dict)
        new_user.password_hash = hashed_passwd
        new_user.role = "user"
        session.add(new_user)
        await session.commit()
        return new_user
