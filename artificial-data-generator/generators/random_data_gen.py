import csv
import random
import string

from config import NAMES_FILE, ORIGINAL_CUSTOMERS, ORIGINAL_PRODUCTS, NO_SIZE_TO_SIZE_RATIO
from generators.generator import Generator


class RandomDataGen(Generator):
    def __init__(self):
        with open(NAMES_FILE, 'r') as f:
            reader = csv.DictReader(f)
            self.names = list([dict(row[1]) for row in enumerate(reader)])

        with open(ORIGINAL_CUSTOMERS, 'r') as f:
            reader = csv.DictReader(f)
            self.customers = list([dict(row[1]) for row in enumerate(reader)])
        
        with open(ORIGINAL_PRODUCTS, 'r') as f:
            reader = csv.DictReader(f)
            self.products = list([dict(row[1]) for row in enumerate(reader)])

    def generate_person(self):
        rname = random.choice(self.names)
        rdata = random.choice(self.customers)
        age = random.randint(18, 90)

        return {
            'name': rname['name'] + ' ' + rdata['name'].split()[-1],
            'gender': rname['gender'],
            'age': age
        }

    def generate_phone_number(self):
        return f'({random.randint(100, 999)}){random.randint(100, 999)}-{random.randint(1000, 9999)}'

    def generate_address(self):
        rdata1 = random.choice(self.customers)
        rdata2 = random.choice(self.customers)
        return {
            'address': str(random.randint(1, 350)) + ' ' + ' '.join(rdata1['address'].split()[1:]),
            'city': rdata2['city'],
            'state': rdata2['state'],
            'postalCode': rdata2['postalCode']
        }

    def generate_size(self):
        if random.random() > NO_SIZE_TO_SIZE_RATIO:
            rdata = random.choice(self.products)
            return rdata['size']
        return 'no size'

    def generate_description(self):
        rdata = random.choice(self.products)
        return rdata['description'] + self.generate_name_like_string()

    def generate_name_like_string(self):
        return ''.join(random.choices(string.ascii_letters+string.digits, k=random.randint(5, 20)))

    def generate(self):
        return {
            'person': self.generate_person(),
            'address': self.generate_address(),
            'phone': self.generate_phone_number()
        }
