from fastapi import APIRouter, Depends, status
from .schemas import User, UserCreate, UserLogin
from.service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from .utils import create_token, decode_token, verify_passwd
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_curr_user, RoleChecker
from datetime import timedelta, datetime, timezone
from src.db.redis import add_token_to_blacklist


REFRESH_TOKEN_EXPIRY=2

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(['admin','user'])


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
            access_token = create_token(
                user_data = {
                    'user_id': str(user.uid),
                    'user_email': user.email
                    'user_role': user.role
                }
            )

            refresh_token = create_token(
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


@auth_router.get('/refresh_token')
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):

    exp_time = token_details['exp']
    print('MIBOMBOOOO: ',datetime.fromtimestamp(exp_time), datetime.now(timezone.utc))
    if datetime.fromtimestamp(exp_time) > datetime.now():
        new_access_token = create_token(
            user_data = token_details['user']
        )

        return JSONResponse(content={
            'access_token': new_access_token
        })

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Invalid or expired refresh token'
    )


@auth_router.get('/me')
async def get_current_user(
    user = Depends(get_current_user),
    _: bool = Depends(role_checker)
):
    return user


@auth_router.get('/logout')
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    token_jti = token_details['jti']
    await add_token_to_blacklist(token_jti)

    return JSONResponse(
        content={
            'message': 'Logged out successfully'
        },
        status_code=status.HTTP_200_OK
    )
