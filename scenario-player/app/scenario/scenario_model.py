from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

STEP_TYPE_MOVE = 'MOVE'
STEP_TYPE_FOCUS = 'FOCUS'
STEP_TYPE_ENTER = 'ENTER'
STEP_TYPE_EXIT = 'EXIT'


class Location(BaseModel):
    """
    Object representing location of the customer in the store.
    """
    x: int = Field(description='coordinate X')
    y: int = Field(description='coordinate Y')


class Step(BaseModel):
    type: str  # TODO: introduce enum/Literal
    location: Location
    timestamp: Optional[datetime]


class CustomerDescription(BaseModel):
    customer_id: str
    # name: Optional[str]
    # gender: Optional[str]
    # age_bucket: Optional[str]
    # preferred_vendors: Optional[List[str]]


class Scenario(BaseModel):
    customer: CustomerDescription
    path: Optional[List[Step]]


class CustomerState(BaseModel):
    customer_description: CustomerDescription
    location: Location
    status: Optional[str] = STEP_TYPE_MOVE
    timestamp: Optional[datetime]


class State(BaseModel):
    customer_states: Optional[List[CustomerState]]


class Timeline(BaseModel):
    name: str
    from_timestamp: int
    to_timestamp: int
