from app.utils import logger
from app.utils.config import CLIENT_ID, AUTO_OFFSET_RESET, BOOTSTRAP_SERVERS, GROUP_ID, DEPARTMENTS
from app.utils.prediction_model import Customer, Coupon


class DummyConsumer:
    def __init__(self, topic_name: str, bootstrap_servers=BOOTSTRAP_SERVERS, group_id=GROUP_ID,
                 client_id: str = CLIENT_ID, auto_offset_reset=AUTO_OFFSET_RESET):
        logger.info(f'DummyConsumer {topic_name}, {bootstrap_servers}, {group_id}, {client_id}, {auto_offset_reset}')
        self.consumer = None
        self.topic = topic_name

    async def process(self, message: str):
        logger.warning('Not implemented.')

    async def consume_messages(self):
        logger.info(f'Pretending messages consumption for {self.topic}')


class DummyProducer:
    def __init__(self, topic_name: str, bootstrap_servers=BOOTSTRAP_SERVERS, client_id: str = CLIENT_ID):
        logger.info(f'DummyProducer {topic_name}, {bootstrap_servers}, {client_id}')
        self.producer = None
        self.topic = topic_name

    def publish_message(self, value: str, key: str = None):
        logger.info(f'pretending to publish_message to topic {self.topic} with key {key}')
        logger.info(value)
        try:
            if key:
                key = key.encode('utf-8')
            if value:
                value = value.encode('utf-8')
            logger.debug(f'Message {value} published.')
        except Exception as ex:
            logger.error(f'Exception in publishing message: {type(ex)} {ex}')


class DummyReadCache:
    def __init__(self):
        logger.info('Creating dummy ReadCache object.')
        pass

    async def read_customer(self, id: int):
        assert type(id) == int
        return Customer(
            customer_id=1,
            age_range='70+',
            marital_status='Married',
            family_size=2,
            no_of_children=0,
            income_bracket=4,
            gender='M',
            mean_discount_used=-1.75,
            total_discount_used=99.22,
            total_unique_items_bought=463,
            total_quantity_bought=99.22,
            mean_quantity_bought=463,
            mean_selling_price_paid=99.22,
            total_coupons_redeemed=1.0,
            total_price_paid=-1832.94,
        )

    async def read_coupons(self, category: str):
        assert category in DEPARTMENTS
        coupon = Coupon(coupon_id=1, coupon_discount=-1.04, item_selling_price=102.22, item_category='Boys')
        return [coupon]
