import pickle
from typing import List

import pandas

from .model import CustomerCouponScore, Customer, Coupon


class Scorer:
    _threshold = 0.2
    _age_range_encoding = {
        '18-25': 0, '26-35': 1, '36-45': 2, '46-55': 3, '56-70': 4, '70+': 5
    }
    _marital_status_encoding = {'Married': 0, 'Single': 1}
    _gender_encoding = {'F': 0, 'M': 1}


    def __init__(self, model):
        self._model = model

    def get_scores(self, customer: Customer, coupons: List[Coupon]) -> List[CustomerCouponScore]:
        input = self._prepare_data(customer=customer, coupons=coupons)
        output = input[['coupon_id', 'customer_id']]
        input.drop(['coupon_id', 'customer_id'], axis=1)
        preds = pandas.Series(self._model.predict(input))
        preds = preds.apply(lambda x: 1 if x > self._threshold else 0)
        output['score'] = preds
        return [
            CustomerCouponScore(coupon_id=r.coupon_id, customer_id=r.customer_id, score=r.score)
            for _, r in output.iterrows()
        ]

    def _prepare_data(self, customer: Customer, coupons: List[Coupon]) -> pandas.DataFrame:
        rows = []
        for c in coupons:
            row = {
                'coupon_id': c.coupon_id,
                'selling_price': c.item_selling_price,
                'coupon_discount': c.discount,
                'category_Boys': 1 if c.category == 'Boys' else 0,
                'category_Girls': 1 if c.category == 'Girls' else 0,
                'category_Men': 1 if c.category == 'Men' else 0,
                'category_Sports': 1 if c.category == 'Sports' else 0,
                'category_Women': 1 if c.category == 'Women' else 0,
                'customer_id': customer.customer_id,
                'age_range': self._age_range_encoding[customer.age_range],
                'marital_status': self._marital_status_encoding[customer.marital_status],
                'family_size': customer.family_size,
                'no_of_children': customer.no_of_children,
                'income_bracket': customer.income_bracket,
                'gender': self._gender_encoding[customer.gender],
                'mean_discount_per_cust': customer.mean_discount_used,
                'total_discount_per_cust': customer.total_discount_used,
                'unique_items_per_cust': customer.unique_items_bought,
                'total_items_per_cust': customer.total_transactions_made,
                'mean_quantity_per_cust': customer.mean_quantity_bought,
                'mean_selling_price_per_cust': customer.mean_selling_price_paid,
                'total_coupons_used_per_cust': customer.total_coupons_redeemed,
                'total_quantity_per_cust': customer.total_quantity_bought,
                'total_selling_price_per_cust': customer.total_price_paid
            }
            rows.append(row)
        return pandas.DataFrame(rows)


def get_scorer():
    model_path = 'app/model_store/scikit_regressor'
    with open(model_path, 'rb') as f:
        return Scorer(pickle.load(f))
