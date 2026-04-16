import asyncio
import asyncpg


class DBConn:

    def __init__(self):
        self.DB_HOST='aws-1-ap-south-1.pooler.supabase.com'
        self.DB_PORT=5432
        self.DB_USER='postgres.ivwdrnltmaxuoyofbdnh'
        self.DB_NAME='postgres'
        self.DB_PASS='getchopaperup'

    async def create_pool(self):
        try:
            pool = await asyncpg.create_pool(
                    host=self.DB_HOST,
                    port=self.DB_PORT,
                    user=self.DB_USER,
                    database=self.DB_NAME,
                    password=self.DB_PASS,
                    max_size=10,
                    min_size=10
            )
            return pool

        except Exception as e:
            print(f'Pool not created, error occured: {e}')
            raise


async def main():
    db = DBConn()
    pool = None
    try:
        pool = await db.create_pool()
        async with pool.acquire() as conn:
            print(f"""
                Connection established.
                Result for SELECT 1: {await conn.fetch('SELECT 1')}
            """)

    except Exception as e:
        print(f'Error occured: {e}')
        import sys
        sys.exit(1)

    finally:
        if pool:
            await pool.close()
            print('Pool closed')


if __name__=="__main__":
    asyncio.run(main())
