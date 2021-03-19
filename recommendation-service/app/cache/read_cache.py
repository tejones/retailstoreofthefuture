import asyncio
import aiopg
import psycopg2

from app.utils.config import DEPARTMENTS
from app.utils import logger

from app.utils.prediction_model import Customer, Coupon


class ReadCache:
    def __init__(self, db_pool):
        self.pool = db_pool

    async def read_customer(self, id: int):
        assert type(id) == int
        conn = await self.pool.acquire()
        cur = await conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
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

        await cur.execute(query)
        customer = dict(await cur.fetchone())
        return Customer(**customer)

    async def read_coupons(self, category: str):
        assert category in DEPARTMENTS
        conn = await self.pool.acquire()
        cur = await conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
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
        await cur.execute(query)
        return [Coupon(**c) for c in await cur.fetchall()]
