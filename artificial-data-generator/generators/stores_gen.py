from generators.generator import Generator
from config import NAMES_FILE, ORIGINAL_CUSTOMERS
from generators.random_data_gen import RandomDataGen


class StoresGen(Generator):
    def __init__(self, number_of_stores):
        self.number_of_stores = number_of_stores
        super().__init__()

    def generate(self):
        self.logger.debug('Generating Stores')
        rdg = RandomDataGen()

        stores = []
        for i in range(1, self.number_of_stores + 1):
            address = rdg.generate_address()

            stores.append({
                'id': i,
                'address': address['address'],
                'city': address['city'],
                'state': address['state'],
                'postalCode': address['postalCode']
            })

        return stores