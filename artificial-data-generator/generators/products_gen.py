import random

from config import DEPARTMENTS, SIZES, COLORS, CATEGORIES, VENDORS
from generators.generator import Generator
from generators.random_data_gen import RandomDataGen


class ProductsGen(Generator):
    def __init__(self, number_of_products):
        self.number_of_products = number_of_products
        self.rdg = RandomDataGen()
        super().__init__()

    def __product_name(self, department_name, category_of_product):
        name = self.rdg.generate_name_like_string()
        color = random.choice(COLORS)
        return f'{name} - {color} {category_of_product} for {department_name}'

    def __product_description(self, name, sizes, vendor):
        return f'{name} by {vendor}. Available sizes {sizes}'

    def generate(self):
        self.logger.debug('Generating Products')

        products = []
        for i in range(1, self.number_of_products + 1):
            department_id = random.randint(1, len(DEPARTMENTS))
            department = DEPARTMENTS[department_id - 1]
            department_name = department['name']
            category_of_product = random.choice(CATEGORIES[department_name])
            sizes = random.choice(SIZES)
            vendor = random.choice(VENDORS)

            buy_price = int(1 / (random.random() + 0.0003) * 100) / 100 + random.randint(0, 10)
            name = self.__product_name(department_name, category_of_product)

            products.append({
                'id': i,
                'name': name,
                'category': category_of_product,
                'sizes': sizes,
                'vendor': vendor,
                'description': self.__product_description(name, sizes, vendor),
                'buy_price': buy_price,
                'department_id': department_id
            })

        return products