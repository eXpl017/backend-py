from redis import asyncio as aioredis
from src.config import config

CACHE_EXPIRY=3600

token_blacklist = aioredis.StrictRedis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=0
)

async def add_token_to_blacklist(jti: str) -> None:
    await token_blacklist.set(
        name=jti,
        value="",
        ex=CACHE_EXPIRY
    )

async def is_token_in_blacklist(jti: str) -> bool:
    is_present = await token_blacklist.get(jti)
    return is_present is not None
