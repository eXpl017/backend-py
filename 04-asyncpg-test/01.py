import asyncio
import asyncpg

from conn import DBConn

CREATE_USERS_TABLE = (
    """
    CREATE TABLE IF NOT EXISTS users(
        user_id SERIAL PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL
    );"""
)

async def main():
    db = DBConn()
    pool = None
    try:
        pool = await db.create_pool()
        async with pool.acquire() as conn:
            status = await conn.execute(CREATE_USERS_TABLE)
        print(status)

    except Exception as e:
        print(f'Error occured: {e}')

    finally:
        if pool:
            await pool.close()
            print('Pool closed')


asyncio.run(main())
