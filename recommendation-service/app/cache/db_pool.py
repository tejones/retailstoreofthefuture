import asyncio
import aiopg

from app.utils.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


class DBPool:
    def __init__(self):
        self.dsn = f'dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST} port={DB_PORT}'
    
    async def create_pool(self):
        self.pool = await aiopg.create_pool(self.dsn)

    def get_pool(self):
        return self.pool
