from typing import List

from pydantic import BaseModel, confloat


class Coupon(BaseModel):
    coupon_id: int
    coupon_type: str
    department: str
    discount: int
    how_many_products_required: int
    product_mean_price: float
    products_available: int


class Customer(BaseModel):
    customer_id: int
    gender: str
    age: int
    mean_buy_price: float
    total_coupons_used: int
    mean_discount_received: float
    unique_products_bought: int
    unique_products_bought_with_coupons: int
    total_items_bought: int


class PredictionInput(BaseModel):
    customer: Customer
    coupons: List[Coupon]


class PredictionOutput(BaseModel):
    coupon_id: int
    customer_id: int
    prediction: confloat(ge=0, le=1)
