from typing import List

from fastapi import Depends, FastAPI

from .coupon_store import CouponStore, get_coupon_store
from .customer_store import CustomerStore, get_customer_store
from .model import Customer, CustomerCouponScore
from .scorer import Scorer, get_scorer


app = FastAPI(
    title='Coupon Recommendation Service'
)


@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.get('/score_coupons', response_model=List[CustomerCouponScore])
def score_coupons(
    customer_id: int,
    coupon_store: CouponStore = Depends(get_coupon_store),
    customer_store: CustomerStore = Depends(get_customer_store),
    scorer: Scorer = Depends(get_scorer)
):
    coupons = coupon_store.list_available_coupons()
    customer_info = customer_store.get(customer_id=customer_id)
    return scorer.get_scores(customer=customer_info, coupons=coupons)
