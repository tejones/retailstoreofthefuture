import csv
import random

from generators.generator import Generator
from generators.random_data_gen import RandomDataGen


class CustomersGen(Generator):
    def __init__(self, number_of_customers, number_of_stores):
        self.number_of_customers = number_of_customers
        self.number_of_stores = number_of_stores
        super().__init__()

    def generate(self):
        self.logger.debug('Generating Customers')
        rdg = RandomDataGen()

        customers = []
        for i in range(1, self.number_of_customers + 1):
            person = rdg.generate_person()
            phone = rdg.generate_phone_number()
            address = rdg.generate_address()

            customers.append({
                'id': i,
                'name': person['name'],
                'gender': person['gender'],
                'age': person['age'],
                'phone': phone,
                'address': address['address'],
                'city': address['city'],
                'state': address['state'],
                'postalCode': address['postalCode'],
                'country': 'US',
                'creditLimit': random.randint(300, 10000)
            })

        return customers
        