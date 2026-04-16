import asyncio
import asyncpg 

from conn import DBConn

GET_USER = (
    """
    SELECT user_id, first_name, last_name
    FROM users
    WHERE user_id=$1
    """
)


async def fetch_user(pool, id):
    async with pool.acquire() as conn:
        return await conn.fetchrow(GET_USER, id)


async def main():
    db = DBConn()
    pool = None
    try:
        pool = await db.create_pool()
        queries = [
            fetch_user(pool,1),
            fetch_user(pool,2)
        ]
        rows: list[asyncpg.Record] = await asyncio.gather(*queries)
        if rows:
            for row in rows:
                print(*row)

    except Exception as e:
        print(f'Error occured: {e}')

    finally:
        if pool:
            await pool.close()
            print('Pool closed')


asyncio.run(main())
