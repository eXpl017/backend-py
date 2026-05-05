import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from src.config import config
from uuid import uuid4


ACCESS_TOKEN_EXPIRY = 30


def hash_passwd(passwd: str) -> str:
    passwd_bytes = passwd.encode()
    salt = bcrypt.gensalt()
    hashed_passwd = bcrypt.hashpw(passwd_bytes, salt)
    return hashed_passwd.decode()

def verify_passwd(login_passwd: str, hashed_passwd: str) -> bool:
    return bcrypt.checkpw(login_passwd.encode(), hashed_passwd.encode())


def create_token(
    user_data: dict,
    expiry: int = ACCESS_TOKEN_EXPIRY,
    refresh: bool = False
):
    payload = {}

    payload['user'] = user_data
    payload['jti'] = str(uuid4())
    payload['refresh'] = refresh
    payload['exp'] = datetime.now(timezone.utc) + (timedelta(days=expiry) if refresh else timedelta(seconds=expiry))

    token = jwt.encode(
        payload=payload,
        key=config.JWT_SECRET,
        algorithm=config.JWT_ALGORITHM
    )

    return token

def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt = token,
            key = config.JWT_SECRET,
            algorithms = [config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        print(f'JWT error occured while decoding: {e}')
        return None
