import pandas

from app.model import PredictionInput


class DataEncoder:
    _gender = ['F', 'M']
    _age = ['young', 'mid', 'old']
    _categories = ['Boys', 'Girls', 'Men', 'Sports', 'Women']
    _coupon_types = ['biy_all', 'boy_more', 'department', 'just_discount']

    @classmethod
    def encode(cls, input: PredictionInput) -> pandas.DataFrame:
        rows = []
        for coupon in input.coupons:
            row = {
                'customer_id': input.customer.customer_id,
                'cust_credit': input.customer.credit,
                'cust_mean_product_price': input.customer.mean_product_price,
                'cust_unique_coupons_used': input.customer.unique_coupons_used,
                'cust_mean_discount': input.customer.mean_discount_used,
                'cust_unique_products_bought': input.customer.unique_items_bought,
                'cust_total_products_bougth': input.customer.total_items_bought,
                'coupon_id': coupon.coupon_id,
                'coupon_discount': coupon.coupon_discount,
                'coupon_how_many': coupon.how_many_products,
                'coupon_days_valid': coupon.days_valid,
                'coupon_mean_prod_price': coupon.mean_item_selling_price
            }
            # row.update(cls._encode_category(coupon.item_category))
            row.update(cls._encode_age(input.customer.age))
            row.update(cls._encode_gender(input.customer.gender))
            row.update(cls._encode_coupon_type(coupon.coupon_type))
            rows.append(row)
        return pandas.DataFrame(rows)

    @classmethod
    def _encode_category(cls, category):
        return {f'category_{c}': 1 if category == c else 0 for c in cls._categories}

    @classmethod
    def _encode_age(cls, age):
        return {f'cust_age_{a}': 1 if age == a else 0 for a in cls._age}

    @classmethod
    def _encode_gender(cls, gender):
        return {f'cust_gender_{g}': 1 if gender == g else 0 for g in cls._gender}

    @classmethod
    def _encode_coupon_type(cls, coupon_type):
        return {f'coupon_type_{t}': 1 if coupon_type == t else 0 for t in cls._coupon_types}
