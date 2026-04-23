from fastapi import APIRouter, Depends, status
from .schemas import User, UserCreate, UserLogin
from.service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from .utils import create_access_token, decode_token, verify_passwd


REFRESH_TOKEN_EXPIRY=2

auth_router = APIRouter()
user_service = UserService()


@auth_router.post(
    '/signup',
    response_model=User,
    status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Creation failed, user email already exists'
        )
    new_user = await user_service.create_user(user_data, session)
    return new_user

@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login_user(
    login_data: UserLogin,
    session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)
    if user is not None:
        password_valid = verify_passwd(password, user.password_hash)
        if password_valid:
            access_token = create_access_token(
                user_data = {
                    'user_id': str(user.uid),
                    'user_email': user.email
                }
            )

            refresh_token = create_access_token(
                user_data = {
                    'user_id': str(user.uid),
                    'user_email': user.email
                },
                expiry = 2,
                refresh = True
            )

            return JSONResponse(
                content = {
                    'message': 'Login Successful',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': {
                        'email': user.email,
                        'uid': str(user.uid)
                    }
                }
            )

    raise HTTPException(
        status = status.HTTP_401_UNAUTHORIZED,
        detail = 'Invalid email address or password'
    )
