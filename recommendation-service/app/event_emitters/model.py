from typing import List, Optional

from pydantic import BaseModel, Field


class Customer(BaseModel):
    id: str = Field(alias='customer_id')


class Product(BaseModel):
    id: str = Field(alias='product_id')
    name: str
    category: str
    sizes: str
    vendor: str
    description: str
    buy_price: float
    department: str


class RecommendedCoupon(BaseModel):
    id: str = Field(alias='coupon_id')
    type: str = Field(alias='coupon_type')
    department: str
    discount: float
    how_many_products_required: int
    start_date: str
    end_date: str
    products: List[Product]


class PredictionResult(BaseModel):
    customer: Customer
    coupon: Optional[RecommendedCoupon]
    ts: int
