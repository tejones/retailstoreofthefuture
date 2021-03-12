from typing import List

from .model import Coupon


class CouponStore:

    def list_available_coupons(self) -> List[Coupon]:
        return [
            Coupon(coupon_id=1, discount=-35.62, item_selling_price=70.88, category='Men'),
            Coupon(coupon_id=2, discount=-26.71, item_selling_price=14.48, category='Women'),
            Coupon(coupon_id=3, discount=-14.25, item_selling_price=14.6, category='Sports')
        ]


def get_coupon_store():
    return CouponStore()
