import aiopg
import psycopg2

from app import logger
from app.config import config
from app.cache.dummy_reader import DummyCacheReader
from app.cache.model import Customer, Coupon, Product


class DBPool:

    def __init__(self, pool):
        self._pool = pool

    @classmethod
    async def create(cls, dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD,
                     host=config.DB_HOST, port=config.DB_PORT):
        dsn = f'dbname={dbname} user={user} password={password} host={host} port={port}'
        pool = await aiopg.create_pool(dsn)
        return DBPool(pool)

    def acquire(self):
        return self._pool.acquire()


class CacheReader:
    _pool = None

    def __init__(self):
        logger.info('Initializing postgres connection.')

    @classmethod
    async def initialize(cls):
        logger.info('Initializing the pool.')
        if cls._pool is None:
            logger.info('Creating new db pool.')
            cls._pool = await DBPool.create()
        else:
            logger.info('Reusing existing db pool.')

    async def read_customer(self, customer_id: int):
        logger.info(f'Read cache for customer {customer_id}')

        query = f'''
                SELECT
                    customer_id,
                    gender,
                    age,
                    mean_buy_price,
                    total_coupons_used,
                    mean_discount_received,
                    unique_products_bought,
                    unique_products_bought_with_coupons,
                    total_items_bought
                FROM customer_info
                    WHERE customer_id = {customer_id};
                '''

        async with self._pool.acquire() as conn:
            async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                await cur.execute(query)
                customer = dict(await cur.fetchone())
        return Customer(**customer)

    async def read_coupons(self, department: str):
        logger.info(f'Read cache for coupons in department {department}')

        query = f'''
                SELECT
                    coupon_id,
                    coupon_type,
                    department,
                    discount,
                    how_many_products_required,
                    product_mean_price,
                    products_available,
                    start_date,
                    end_date
                FROM coupon_info
                WHERE department = '{department}';
                '''

        async with self._pool.acquire() as conn:
            async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                await cur.execute(query)
                return [Coupon(**c) for c in await cur.fetchall()]

    async def read_products(self, coupon_id: int):
        query = f'''
            SELECT
                pi.product_id,
                pi.name,
                pi.category,
                pi.sizes,
                pi.vendor,
                pi.description,
                pi.buy_price,
                pi.department
            FROM product_info pi JOIN coupon_product cp
                ON pi.product_id = cp.product_id
            WHERE cp.coupon_id = {coupon_id};
        '''

        async with self._pool.acquire() as conn:
            async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                await cur.execute(query)
                return [Product(**p) for p in await cur.fetchall()]


async def create_cache_reader():
    if config.TESTING_NO_POSTGRES:
        rc = DummyCacheReader()
    else:
        rc = CacheReader()
        await rc.initialize()
    return rc
