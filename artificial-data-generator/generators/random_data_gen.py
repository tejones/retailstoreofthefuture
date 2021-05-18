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
        syllables = [
            'AL', 'AL', 'AN', 'AN', 'AR', 'AR', 'AS', 'AS', 'AT', 'AT', 'EA', 'EA', 'ED', 'ED', 'EN', 'EN', 'ER',
            'ER', 'ES', 'ES', 'HA', 'HA', 'HE', 'HE', 'HI', 'HI', 'IN', 'IN', 'IS', 'IS', 'IT', 'IT', 'LE', 'LE',
            'ME', 'ME', 'ND', 'ND', 'NE', 'NE', 'NG', 'NG', 'NT', 'NT', 'ON', 'ON', 'OR', 'OR', 'OU', 'OU',
            'RE', 'RE', 'SE', 'SE', 'ST', 'ST', 'TE', 'TE', 'TH', 'TH', 'TI', 'TI', 'TO', 'TO', 'VE', 'VE',
            'WA', 'WA', 'ALL', 'ALL', 'AND', 'AND', 'ARE', 'ARE', 'BUT', 'BUT', 'ENT', 'ENT', 'ERA', 'ERA', 'ERE',
            'ERE', 'EVE', 'EVE', 'FOR', 'FOR', 'HAD', 'HAD', 'HAT', 'HAT', 'HEN', 'HEN', 'HER', 'HER', 'HIN', 'HIN',
            'HIS', 'HIS', 'ING', 'ING', 'ION', 'ION', 'ITH', 'ITH', 'NOT', 'NOT', 'OME', 'OME', 'OUL', 'OUL', 'OUR',
            'OUR', 'SHO', 'SHO', 'TED', 'TED', 'TER', 'TER', 'THA', 'THA', 'THE', 'THE', 'THI', 'THI', 'TIO', 'TIO',
            'ULD', 'ULD', 'VER', 'VER', 'WAS', 'WAS', 'WIT', 'WIT', 'YOU', 'YOU', 'TH', 'TH', 'HE', 'HE', 'AN', 'AN',
            'ER', 'ER', 'IN', 'IN', 'RE', 'RE', 'ND', 'ND', 'OU', 'OU', 'EN', 'EN', 'ON', 'ON', 'ED', 'ED', 'TO', 'TO',
            'IT', 'IT', 'AT', 'AT', 'HA', 'HA', 'VE', 'VE', 'AS', 'AS', 'OR', 'OR', 'HI', 'HI', 'AR', 'AR', 'TE', 'TE',
            'ES', 'ES', 'NG', 'NG', 'IS', 'IS', 'ST', 'ST', 'LE', 'LE', 'AL', 'AL', 'TI', 'TI', 'SE', 'SE', 'EA', 'EA',
            'WA', 'WA', 'ME', 'ME', 'NT', 'NT', 'NE', 'NE'
        ]
        return ''.join(random.choices(syllables, k=random.randint(2, 5)))

    def generate(self):
        return {
            'person': self.generate_person(),
            'address': self.generate_address(),
            'phone': self.generate_phone_number()
        }
