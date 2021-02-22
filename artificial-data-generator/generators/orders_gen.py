from datetime import datetime, timedelta
import random

from config import STORE_HOURS_OPEN, DATETIME_FORMAT
from generators.generator import Generator


class OrdersGen(Generator):
    def __init__(self, number_of_stores,
            customer_preferences, products, start_date, end_date):
        self.number_of_stores = number_of_stores
        self.customer_preferences = customer_preferences
        self.products = products
        self.products_tree = self.__prod_tree(products)
        self.start_date = start_date
        self.end_date = end_date
        super().__init__()

    def __select_dist(self, dist):
        r = random.random()
        s = 0
        for element in dist:
            s += element[1]
            if s >= r:
                return element[0]
        return 1

    def __prod_tree(self, products):
        prod_tree = {}
        for product in products:
            if product['productVendor'] not in prod_tree.keys():
                prod_tree[product['productVendor']] = {}
            
            if product['departmentCode'] not in prod_tree[product['productVendor']].keys():
                prod_tree[product['productVendor']][product['departmentCode']] = {}
            
            if product['category'] not in prod_tree[product['productVendor']][product['departmentCode']].keys():
                prod_tree[product['productVendor']][product['departmentCode']][product['category']] = []
            
            prod_tree[product['productVendor']][product['departmentCode']][product['category']].append(product['id'])
        return prod_tree

    def generate(self):
        self.logger.debug('Generating Orders')
        current = self.start_date

        oid = 1
        odid = 1
        orders = []
        order_details = []
        while self.end_date > current:
            for h in range(0, STORE_HOURS_OPEN):
                for customer in self.customer_preferences:
                    if (customer['orderProbPref'] if current.weekday() == customer['day']
                            else customer['orderProbNormal'])/STORE_HOURS_OPEN > random.random():
                        orders.append({
                            'id': oid,
                            'customerId': customer['customerId'],
                            'orderDate': (current + timedelta(seconds=random.randint(0, 3600))).strftime(DATETIME_FORMAT)
                        })
                        prod_nr = customer['avgProductsPerOrder'] + random.randint(0, 8) - 4

                        for _ in range(prod_nr):
                            vendor = self.__select_dist(customer['vendors'])
                            department = self.__select_dist(customer['departments'])
                            category = self.__select_dist(customer['categories'])

                            if vendor not in self.products_tree.keys():
                                vendor = random.choice(list(self.products_tree.keys()))
                            
                            if department not in self.products_tree[vendor].keys():
                                department = random.choice(list(self.products_tree[vendor].keys()))

                            if category not in self.products_tree[vendor][department].keys():
                                category = random.choice(list(self.products_tree[vendor][department].keys()))

                            selected_product_index = random.choice(self.products_tree[vendor][department][category]) - 1

                            order_details.append({
                                'id': odid,
                                'orderId': oid,
                                #################################################################################
                                'productId': self.products[selected_product_index]['id'], # NEEDS TO BE VERIFIED! #
                                'quantityOrdered': random.randint(1, 50), 
                                'msrp': self.products[selected_product_index]['msrp'],
                                'discount': 0 # NEEDS TO BE CHANGED! #
                                #################################################################################
                            })
                            odid += 1
                        oid += 1
                current += timedelta(hours=1)
            current += timedelta(hours=24 - STORE_HOURS_OPEN)

        return orders, order_details
