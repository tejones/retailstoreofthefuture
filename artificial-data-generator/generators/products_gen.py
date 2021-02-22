import random

from generators.generator import Generator
from generators.random_data_gen import RandomDataGen
from config import MSRP_DIFF_RATIO


class ProductsGen(Generator):
    def __init__(self, number_of_products, number_of_departments, number_of_vendors, number_of_categories):
        self.number_of_products = number_of_products
        self.number_of_departments = number_of_departments
        self.number_of_vendors = number_of_vendors
        self.number_of_categories = number_of_categories
        super().__init__()

    def generate(self):
        self.logger.debug('Generating Products')
        rdg = RandomDataGen()

        products = []
        for i in range(1, self.number_of_products + 1):
            buy_price = int(1 / (random.random() + 0.0003) * 100) / 100 + random.randint(0, 10)
            
            if random.random() > MSRP_DIFF_RATIO:
                msrp = buy_price
            else:
                msrp = buy_price * (random.randint(5, 125) / 100)

            products.append({
                'id': i,
                'productName': rdg.generate_name_like_string(),
                'productSize': rdg.generate_size(),
                'productVendor': random.randint(1, self.number_of_vendors),
                'productDescription': rdg.generate_description(),
                'buyPrice': buy_price,
                'msrp': msrp,
                'departmentCode': random.randint(1, self.number_of_departments),
                'category': random.randint(1, self.number_of_categories)
            })

        return products