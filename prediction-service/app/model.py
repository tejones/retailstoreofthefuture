from typing import List

from pydantic import BaseModel, confloat


class Coupon(BaseModel):
    coupon_id: int
    mean_item_selling_price: float
    coupon_discount: float
    category: str  # TODO this is not used (for now)
    how_many_products: int
    coupon_type: str
    days_valid: int


class Customer(BaseModel):
    customer_id: int
    age: str  # TODO Enum
    credit: int
    gender: str  # TODO Enum
    mean_product_price: float
    unique_coupons_used: int
    mean_discount_used: float
    unique_items_bought: int
    total_items_bought: int

class PredictionInput(BaseModel):
    customer: Customer
    coupons: List[Coupon]


class PredictionOutput(BaseModel):
    coupon_id: int
    customer_id: int
    prediction: confloat(ge=0, le=1)
