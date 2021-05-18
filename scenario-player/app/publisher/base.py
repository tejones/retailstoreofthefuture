from app import logger
from app.scenario.scenario_model import CustomerState


class BaseEventPublisher:

    async def initialize(self):
        """
        Initialize the backend (for example, connect to the DB, etc.)
        :return:
        """
        raise NotImplemented

    def prepare_payload(self, customer_state: CustomerState):
        return str(customer_state)

    async def publish_state(self, customer_state: CustomerState):
        raise NotImplemented


class LoggerEventPublisher(BaseEventPublisher):

    async def initialize(self):
        pass

    async def publish_state(self, customer_state: CustomerState):
        message = self.prepare_payload(customer_state)
        logger.info(f'Publishing {message}')
