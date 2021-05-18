from pydantic import BaseModel, Field


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


class Product(BaseModel):
    product_id: int
    name: str
    category: str
    sizes: str
    vendor: str
    description: str
    buy_price: float
    department: str


class Coupon(BaseModel):
    coupon_id: int
    coupon_type: str
    department: str
    discount: float
    how_many_products_required: int
    product_mean_price: float
    products_available: int
    start_date: str
    end_date: str
