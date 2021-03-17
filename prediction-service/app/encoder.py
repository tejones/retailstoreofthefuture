import pandas

# from .model import PredictionInput
from app.model import PredictionInput


class DataEncoder:
    _age_range = {'18-25': 0, '26-35': 1, '36-45': 2, '46-55': 3, '56-70': 4, '70+': 5}
    _marital_status = {'Married': 0, 'Single': 1}
    _gender = {'F': 0, 'M': 1}
    _categories = ['Boys', 'Girls', 'Men', 'Sports', 'Women']

    @classmethod
    def encode(cls, input: PredictionInput) -> pandas.DataFrame:
        rows = []
        for coupon in input.coupons:
            row = {
                'customer_id': input.customer.customer_id,
                'age_range': cls._age_range[input.customer.age_range],
                'marital_status': cls._marital_status[input.customer.marital_status],
                'family_size': input.customer.family_size,
                'no_of_children': input.customer.no_of_children,
                'income_bracket': input.customer.income_bracket,
                'gender': cls._gender[input.customer.gender],
                'mean_discount_per_cust': input.customer.mean_discount_used,
                'unique_items_per_cust': input.customer.total_unique_items_bought,
                'mean_quantity_per_cust': input.customer.mean_quantity_bought,
                'mean_selling_price_per_cust': input.customer.mean_selling_price_paid,
                'total_discount_per_cust': input.customer.total_discount_used,
                'total_coupons_used_per_cust': input.customer.total_coupons_redeemed,
                'total_quantity_per_cust': input.customer.total_quantity_bought,
                'total_selling_price_per_cust': input.customer.total_price_paid,
                'coupon_id': coupon.coupon_id,
                # TODO coupon_discount: coupon.coupon_discount
                # TODO item_selling_price: coupon.item_selling_price
            }
            row.update(cls._encode_category(coupon.item_category))
            rows.append(row)

        return pandas.DataFrame(rows)

    @classmethod
    def _encode_category(cls, category):
        return {f'category_{c}': 1 if category == c else 0 for c in cls._categories}
