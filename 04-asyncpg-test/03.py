import asyncio
import asyncpg

from conn import DBConn

SELECT_USERS = (
    """
    SELECT user_id, first_name, last_name 
    FROM users;"""
)

async def main():
    db = DBConn()
    pool = None
    try:
        pool = await db.create_pool()
        async with pool.acquire() as conn:
            rows: list[asyncpg.Record] = await conn.fetch(SELECT_USERS)

        for row in rows:
            print(*row)

    except Exception as e:
        print(f'Error occured: {e}')

    finally:
        if pool:
            await pool.close()
            print('Pool closed')

asyncio.run(main())
