from datetime import datetime, timezone
from typing import Optional, List

from pydantic import BaseModel, Field
from pydantic.datetime_parse import parse_datetime

STEP_TYPE_MOVE = 'MOVE'
STEP_TYPE_FOCUS = 'FOCUS'
STEP_TYPE_ENTER = 'ENTER'
STEP_TYPE_EXIT = 'EXIT'


class UtcDatetime(datetime):
    @classmethod
    def __get_validators__(cls):
        yield parse_datetime
        yield cls.ensure_tzinfo

    @classmethod
    def ensure_tzinfo(cls, v):
        if v.tzinfo is None:
            raise ValueError('The datetime should have timezone info')
        # convert the timezone to utc
        return v.astimezone(timezone.utc)

    @staticmethod
    def to_str(dt: datetime) -> str:
        return dt.isoformat()


class Location(BaseModel):
    """
    Object representing location of the customer in the store.
    """
    x: int = Field(description='coordinate X')
    y: int = Field(description='coordinate Y')


class Step(BaseModel):
    type: str  # TODO: introduce enum/Literal
    location: Location
    timestamp: Optional[UtcDatetime] = Field(description='timezone aware timestamp of the event')


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
    timestamp: Optional[UtcDatetime]


class State(BaseModel):
    customer_states: Optional[List[CustomerState]]


class Timeline(BaseModel):
    name: str
    from_timestamp: int
    to_timestamp: int
