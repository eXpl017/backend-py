import asyncio
import asyncpg

from conn import DBConn

# will give error as user at ID already exists
INSERT_STMT = (
    """
    INSERT INTO users
    VALUES(1, 'random', 'guy');"""
)


async def main():
    db = DBConn()
    pool, conn = None, None
    try:
        pool = await db.create_pool()
        conn = await pool.acquire()
        #async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(INSERT_STMT)
    except Exception as e:
        print(f'Error occured: {e}')

    finally:

        # when you acquire a conn from pool, you need to release it
        # closing it and releasing it are different
        # closing will close to the conn, and not return anything to pool
        # release will safely return the connection back into the pool for further usage
        if conn and pool:
            await pool.release(conn)
        if pool:
            await pool.close()
            print('Pool closed')


asyncio.run(main())
