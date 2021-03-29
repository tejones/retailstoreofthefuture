import aiopg
import psycopg2

from app.utils import logger
from app.utils.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from app.utils.config import DEPARTMENTS
from app.utils.prediction_model import Customer, Coupon


class DBPool:
    @classmethod
    async def create(cls, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT):
        self = DBPool()
        self.dsn = f'dbname={dbname} user={user} password={password} host={host} port={port}'
        self.pool = await aiopg.create_pool(self.dsn)
        return self

    def get_pool(self):
        return self.pool


class ReadCache:
    pool = None

    def __init__(self):
        pass

    async def initialize(self):
        logger.info('Initializing the pool.')
        if not ReadCache.pool:
            logger.info('Creating new db pool.')
            ReadCache.pool = await DBPool.create()
        else:
            logger.info('Reusing existing db pool.')

    async def read_customer(self, id: int):
        logger.info(f'read customer {id}')

        query = f'''
                SELECT
                    customer_id,
                    age_range,
                    marital_status,
                    family_size,
                    no_of_children,
                    income_bracket,
                    gender,
                    mean_discount_used_by_cust mean_discount_used,
                    total_discount_used_by_cust total_discount_used,
                    unique_items_bought_by_cust total_unique_items_bought,
                    total_quantity_bought_by_cust total_quantity_bought,
                    mean_quantity_bought_by_cust mean_quantity_bought,
                    mean_selling_price_paid_by_cust mean_selling_price_paid,
                    total_coupons_used_by_cust total_coupons_redeemed,
                    total_price_paid_by_cust total_price_paid
                FROM customer_info
                    WHERE customer_id = {id}
                '''

        assert type(id) == int
        async with ReadCache.pool.get_pool().acquire() as conn:
            async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                await cur.execute(query)
                customer = dict(await cur.fetchone())
        return Customer(**customer)

    async def read_coupons(self, category: str):
        assert category in DEPARTMENTS

        query = f'''
                SELECT DISTINCT
                    cc.coupon_id,
                    cc.category item_category,
                    ci.mean_item_price item_selling_price,
                    ci.mean_coupon_discount coupon_discount
                FROM coupon_categories cc INNER JOIN coupon_info ci
                    ON cc.coupon_id = ci.coupon_id
                    WHERE cc.category='{category}'
                '''

        async with ReadCache.pool.get_pool().acquire() as conn:
            async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                await cur.execute(query)
                return [Coupon(**c) for c in await cur.fetchall()]
        return None
