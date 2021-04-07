from pydantic import BaseModel
from typing import List, Optional

from app.events_model import CustomerEvent


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
    age_bucket: Optional[str]
    preferred_vendors: Optional[List[str]]


class Scenario(BaseModel):
    customer: CustomerDescription
    path: Optional[List[Point]]


class CustomerEventExtended(BaseModel):
    customer: CustomerDescription
    location: Optional[Location]
    event_type: str
