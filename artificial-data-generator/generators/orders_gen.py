from datetime import datetime, timedelta
from functools import reduce
import random

from config import STORE_OPEN_HOURS, DATETIME_FORMAT, COUPON_TYPES
from generators.generator import Generator


class OrdersGen(Generator):
    def __init__(self, customer_preferences, products, coupons, start_date, end_date):
        self.customer_preferences = customer_preferences
        self.products = products
        self.products_tree = self.__prod_tree(products)
        self.coupon_tree = self.__coupon_tree(coupons, products)
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
            if product['vendor'] not in prod_tree.keys():
                prod_tree[product['vendor']] = {}
            
            if product['department_id'] not in prod_tree[product['vendor']].keys():
                prod_tree[product['vendor']][product['department_id']] = {}
            
            if product['category'] not in prod_tree[product['vendor']][product['department_id']].keys():
                prod_tree[product['vendor']][product['department_id']][product['category']] = []
            
            prod_tree[product['vendor']][product['department_id']][product['category']].append(product['id'])
        return prod_tree

    def __coupon_tree(self, coupons, products):
        coupon_tree = {}
        for i, coupon in enumerate(coupons):
            for pid in coupon['products']:
                product = products[pid - 1]

                if product['department_id'] not in coupon_tree.keys():
                    coupon_tree[product['department_id']] = {}
                
                if product['category'] not in coupon_tree[product['department_id']].keys():
                    coupon_tree[product['department_id']][product['category']] = {}
                
                if product['vendor'] not in coupon_tree[product['department_id']][product['category']].keys():
                    coupon_tree[product['department_id']][product['category']][product['vendor']] = {}
                
                if pid not in coupon_tree[product['department_id']][product['category']][product['vendor']].keys():
                    coupon_tree[product['department_id']][product['category']][product['vendor']][pid] = []

                coupon_tree[product['department_id']][product['category']][product['vendor']][pid].append({
                    'coupon_id': i + 1,
                    'original_price': product['buy_price'],
                    'discount': coupon['discount'],
                    'type': coupon['type'],
                    'products': coupon['products'],
                    'how_many': coupon['how_many'],
                    'start_date': coupon['start_date'],
                    'end_date': coupon['end_date']
                })
        return coupon_tree

    def __weight_coupons(self, coupons, additional_weight=1):
        return [(
            -(coupon['original_price'] * (1 - (coupon['discount'] / 100))) * (1 / additional_weight) *\
                (1 / COUPON_TYPES[coupon['type']]['probability_of_usage']),
            coupon
        ) for coupon in coupons]

    def __valid_coupons_only(self, current, sim_coupons):
        return [c for c in sim_coupons if c['start_date'] <= current.date() and c['end_date'] >= current.date()]

    def generate(self):
        self.logger.debug('Generating Orders')
        current = self.start_date

        oid = 1
        odid = 1
        orders = []
        order_details = []
        # for each day in range
        while self.end_date > current:
            print(f'Day: {current}') # TODO: change to logger
            # every hour when store is opened
            for h in range(0, STORE_OPEN_HOURS):
                # each customer
                for customer in self.customer_preferences:
                    # can potentially enter the store and buy something
                    if (customer['order_prob_pref'] if current.weekday() == customer['day']
                            else customer['order_prob_normal'])/STORE_OPEN_HOURS > random.random():
                        # and if she/he did, generate order:
                        orders.append({
                            'id': oid,
                            'customer_id': customer['customer_id'],
                            'order_date': (current + timedelta(seconds=random.randint(0, 3600))).strftime(DATETIME_FORMAT)
                        })
                        # buy x products (never < 1)
                        prod_nr = (customer['avg_products_per_order'] + random.randint(0, 8) - 4)
                        prod_nr = 1 if prod_nr <= 0 else prod_nr

                        # generate x positions on the order
                        for _ in range(prod_nr):
                            # select the vendor, department, and category following customer's preferences
                            vendor = self.__select_dist(customer['vendors'])
                            department = self.__select_dist(customer['departments'])
                            category = self.__select_dist(customer['categories'])

                            if vendor not in self.products_tree.keys():
                                vendor = random.choice(list(self.products_tree.keys()))
                            
                            if department not in self.products_tree[vendor].keys():
                                department = random.choice(list(self.products_tree[vendor].keys()))

                            if category not in self.products_tree[vendor][department].keys():
                                category = random.choice(list(self.products_tree[vendor][department].keys()))

                            # and select the product
                            selected_products_ids = [random.choice(self.products_tree[vendor][department][category])]

                            # potential coupon for this buy
                            coupon = None

                            # are we going to use any coupon at all?
                            if random.random() < customer['coupon_usage_probability']:
                                coupons = []

                                # are there any coupons for this product or similar one?
                                try:
                                    for vendor, products in self.coupon_tree[department][category].items():
                                        for sim_product_id, sim_coupons in products.items():
                                            sim_coupons_at_date = self.__valid_coupons_only(current, sim_coupons)
                                            # if(len(sim_coupons) != len(sim_coupons_at_date)):
                                            #     print(current)
                                            #     print(sim_coupons)
                                            #     print(sim_coupons_at_date)
                                            #     print('-'*100)
                                            w = 1 if sim_product_id == selected_products_ids[0] else 0.75
                                            coupons += self.__weight_coupons(sim_coupons_at_date, w)
                                except KeyError:
                                    # logger.debug('No coupons for similar products') # TODO: logger
                                    pass

                                # sort coupons and select final products
                                if len(coupons):
                                    try:
                                        # if len(coupons):
                                        #     print(selected_products_ids[0], coupons)
                                        coupon = sorted(coupons, key=lambda c: c[0])[0][1]
                                        if random.random() < COUPON_TYPES[coupon['type']]['probability_of_usage']:
                                            selected_products_ids = coupon['products']
                                        else:
                                            coupon = None
                                    except IndexError:
                                        # logger.debug('No coupons for product') # TODO: logger
                                        pass

                            ct = coupon['type'] if coupon else None
                            for product_id in selected_products_ids:
                                op = self.products[product_id - 1]['buy_price']
                                order_details.append({
                                    'id': odid,
                                    'order_id': oid,
                                    'product_id': product_id,
                                    'quantity_ordered': coupon['how_many'] if ct else random.randint(1, 20),
                                    'original_price': op,
                                    'buy_price': op * (100 - coupon['discount']) / 100 if ct else op,
                                    'coupon_id': coupon['coupon_id'] if ct else None
                                })
                                odid += 1
                        oid += 1
                current += timedelta(hours=1)
            current += timedelta(hours=24 - STORE_OPEN_HOURS)

        return orders, order_details
