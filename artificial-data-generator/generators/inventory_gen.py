import random

from generators.generator import Generator
from generators.random_data_gen import RandomDataGen
from config import PRODUCTS_PERCENTAGE_IN_STORE_MIN, PRODUCTS_PERCENTAGE_IN_STORE_MAX


class InventoryGen(Generator):
    def __init__(self, number_of_products):
        self.number_of_products = number_of_products
        super().__init__()

    def generate(self):
        self.logger.debug('Generating Inventory')
        inventory = []
        for product in range(1, self.number_of_products):
            inventory.append({
                'productId': product,
                'quantity': random.randint(0, 100)
            })

        return inventory