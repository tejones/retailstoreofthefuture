from pydantic import BaseModel
from typing import List, Optional


class Location(BaseModel):
    x: int
    y: int


class Point(BaseModel):
    type: str
    location: Location
    timestamp: Optional[int]


class CustomerDescription(BaseModel):
    customer_id: str
    name: Optional[str]
    gender: Optional[str]
    age: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postalCode: Optional[int]
    country: Optional[str]
    creditLimit: Optional[int]


class Product(BaseModel):
    id: int
    name: str
    category: str
    sizes: str
    vendor: str
    description: str
    buy_price: float
    department: str


class CouponDescription(BaseModel):
    id: int
    type: str
    department: str
    discount: float
    how_many: int
    start_date: str
    end_date: str
    products: Optional[List[Product]]


class CouponsByDepartment(BaseModel):
    department: str
    coupons: List[CouponDescription]


class Scenario(BaseModel):
    customer: CustomerDescription
    path: Optional[List[Point]]
