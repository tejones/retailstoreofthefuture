from app import logger
from app.config import config
from app.cache.model import Customer, Coupon, Product


class DummyCacheReader:
    
    def __init__(self):
        logger.warning('- ' * 20)
        logger.warning('')
        logger.warning('Initializing fake postgres connection.')
        logger.warning('Please don\'t be fooled!')
        logger.warning('')
        logger.warning('- ' * 20)

    async def read_customer(self, customer_id: int):
        assert type(customer_id) == int
        return Customer(
            customer_id=customer_id,
            gender='F',
            age=40,
            mean_buy_price=15.67,
            total_coupons_used=123,
            mean_discount_received=35.5,
            unique_products_bought=58,
            unique_products_bought_with_coupons=45,
            total_items_bought=520
        )

    async def read_coupons(self, department: str):
        assert department in config.DEPARTMENTS
        coupon = Coupon(
            coupon_id=1,
            coupon_type='buy_all',
            department=department,
            discount=30,
            how_many_products_required=3,
            product_mean_price=12.56,
            products_available=156,
            start_date='12-12-2020',
            end_date='20-01-2021')
        return [coupon]

    async def read_products(self, coupon_id: int):
        assert type(coupon_id) == int
        return [Product(
            product_id=1,
            name='Hat',
            category='Accessories',
            sizes='One Size',
            vendor='Mango',
            description='***',
            buy_price=12.45,
            department='Women'
        )]
