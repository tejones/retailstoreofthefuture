import pandas

from app.model import PredictionInput


class DataEncoder:
    _gender = ['F', 'M']
    _age = ['young', 'mid', 'old']
    _departments = ['Boys', 'Girls', 'Men', 'Sports', 'Women']
    _coupon_types = ['buy_all', 'buy_more', 'department', 'just_discount']

    @classmethod
    def encode(cls, input: PredictionInput) -> pandas.DataFrame:
        rows = []
        for coupon in input.coupons:
            row = {
                'customer_id': input.customer.customer_id,
                'cust_mean_buy_price': input.customer.mean_buy_price,
                'cust_total_coupons': input.customer.total_coupons_used,
                'cust_mean_discount': input.customer.mean_discount_received,
                'cust_unique_products': input.customer.unique_products_bought,
                'cust_unique_products_coupon': input.customer.unique_products_bought_with_coupons,
                'cust_total_products': input.customer.total_items_bought,
                'coupon_id': coupon.coupon_id,
                'coupon_discount': coupon.discount,
                'coupon_how_many': coupon.how_many_products_required,
                'coupon_mean_prod_price': coupon.product_mean_price,
                'coupon_prods_avail': coupon.products_available
            }
            row.update(cls._encode_age(input.customer.age))
            row.update(cls._encode_gender(input.customer.gender))
            row.update(cls._encode_coupon_type(coupon.coupon_type))
            row.update(cls._encode_department(coupon.department))
            rows.append(row)
        return pandas.DataFrame(rows)

    @classmethod
    def _encode_department(cls, department):
        return {f'coupon_dpt_{d}': 1 if department == d else 0 for d in cls._departments}

    @classmethod
    def _encode_age(cls, age):
        if age < 30:
            age_bracket = 'young'
        elif 30 <= age < 50:
            age_bracket = 'mid'
        else:
            age_bracket = 'old'
        return {f'cust_age_{a}': 1 if age_bracket == a else 0 for a in cls._age}

    @classmethod
    def _encode_gender(cls, gender):
        return {f'cust_gender_{g}': 1 if gender == g else 0 for g in cls._gender}

    @classmethod
    def _encode_coupon_type(cls, coupon_type):
        return {f'coupon_type_{t}': 1 if coupon_type == t else 0 for t in cls._coupon_types}
