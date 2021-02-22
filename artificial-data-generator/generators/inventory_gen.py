import random

from generators.generator import Generator
from generators.random_data_gen import RandomDataGen
from config import PRODUCTS_PERCENTAGE_IN_STORE_MIN, PRODUCTS_PERCENTAGE_IN_STORE_MAX


class InventoryGen(Generator):
    def __init__(self, number_of_stores, number_of_products):
        self.number_of_stores = number_of_stores
        self.number_of_products = number_of_products
        super().__init__()

    def generate(self):
        self.logger.debug('Generating Inventory')
        inventory = []
        for store in range(1, self.number_of_stores + 1):
            probability = (PRODUCTS_PERCENTAGE_IN_STORE_MAX - PRODUCTS_PERCENTAGE_IN_STORE_MIN) \
                * random.random() + PRODUCTS_PERCENTAGE_IN_STORE_MIN
            for product in range(1, self.number_of_products):
                if random.random() < probability:
                    inventory.append({
                        'storeId': store,
                        'productId': product,
                        'quantity': random.randint(1, 100)
                    })

        return inventory