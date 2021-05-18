import random
from datetime import timedelta

from config import DEPARTMENTS, COUPONS_PER_DEPARTMENT, COUPON_TYPES, VENDORS
from generators.generator import Generator


class CouponGen(Generator):
    def __init__(self, start_date, end_date, number_of_products):
        super().__init__()

        self.start_date = start_date
        self.end_date = end_date
        self.number_of_products = number_of_products
    
    def __generate_coupon(self):
        pass

    def generate(self):
        coupons = []
        coupon_types = [t for t, d in COUPON_TYPES.items() if d['gen_coupons']]

        current = self.start_date

        coupons_counter = {}
        for department in DEPARTMENTS:
            coupons_counter[department['name']] = [0 for _ in range(COUPONS_PER_DEPARTMENT)]

        cid = 1
        while self.end_date > current:
            for department, coupon_counters in coupons_counter.items():
                for i, cc in enumerate(coupon_counters):
                    coupon_counters[i] -= 1
                    if cc == 0:
                        coupon_len = random.randint(1, 30)
                        ct = random.choice(coupon_types)
                        coupon_info = COUPON_TYPES[ct]

                        vendor = None
                        products = []
                        discount = random.randint(coupon_info['min_discount_percentage'],\
                            coupon_info['max_discount_percentage'])

                        if ct == 'department':
                            how_many = -1
                        elif ct == 'just_discount':
                            products = [random.randint(1, self.number_of_products)]
                            how_many = 1
                        elif ct == 'buy_more':
                            products = [random.randint(1, self.number_of_products)]
                            how_many = random.randint(COUPON_TYPES['buy_more']['min_products'], COUPON_TYPES['buy_more']['max_products'])
                        elif ct == 'buy_all':
                            vendor = random.choice(VENDORS)
                            np = random.randint(coupon_info['min_products'], coupon_info['max_products'])
                            products = [random.randint(1, self.number_of_products) for _ in range(np)]
                            how_many = len(products)

                        coupons.append({
                            'id': cid,
                            'type': ct,
                            'products': products,
                            'discount': discount,
                            'how_many': how_many,
                            'start_date': current.date(),
                            'end_date': (current.date() + timedelta(days=(coupon_len - 1)))
                        })
                        cid += 1
                        coupon_counters[i] = coupon_len

            current += timedelta(days=1)

        return coupons
