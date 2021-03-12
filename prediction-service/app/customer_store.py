from typing import List

from .model import Customer


class CustomerStore:

    def get(self, customer_id: int) -> Customer:
        return Customer(
            customer_id=464,
            age_range='46-55',
            marital_status='Married',
            family_size=5,
            no_of_children=3,
            income_bracket=3,
            gender='M',
            mean_discount_used=-1.83,
            total_discount_used=-7548.79,
            unique_items_bought=2040,
            total_transactions_made=4134,
            mean_quantity_bought=1.04,
            total_quantity_bought=4314,
            mean_selling_price_paid=61.27,
            total_coupons_redeemed=220,
            total_price_paid=253295.6
        )


def get_customer_store():
    return CustomerStore()
