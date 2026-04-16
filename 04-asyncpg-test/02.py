import asyncio
import asyncpg

from conn import DBConn

async def main():
    db = DBConn()
    pool = None
    try:
        pool = await db.create_pool()
        async with pool.acquire() as conn:
            await conn.execute("INSERT INTO users VALUES(DEFAULT, 'lol', 'lmao');")
            await conn.execute("INSERT INTO users VALUES(DEFAULT, 'ded', 'xD');")
            print('Values added.')

    except Exception as e:
        print(f'Error occured: {e}')

    finally:
        if pool:
            await pool.close()
            print('Pool closed')

asyncio.run(main())
