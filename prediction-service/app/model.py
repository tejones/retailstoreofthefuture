from pydantic import BaseModel, conint


class Coupon(BaseModel):
    coupon_id: int
    discount: float
    item_selling_price: float
    category: str


class Customer(BaseModel):
    customer_id: int
    age_range: str  # TODO Enum
    marital_status: str # TODO Enum
    family_size: int
    no_of_children: int
    income_bracket: int
    gender: str  # TODO Enum
    mean_discount_used: float
    total_discount_used: float
    unique_items_bought: int
    total_quantity_bought: int
    total_transactions_made: int
    mean_quantity_bought: float
    mean_selling_price_paid: float
    total_coupons_redeemed: int
    total_price_paid: float


class CustomerCouponScore(BaseModel):
    coupon_id: int
    customer_id: int
    score: conint(ge=0, le=1)
