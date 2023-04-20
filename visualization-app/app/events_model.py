from pydantic import BaseModel
from typing import Optional

from app.data_models import Location, CustomerDescription


class CustomerEvent(BaseModel):
    """
     id: --ID representing customer--,
     ts: --timestamp of the event in seconds in epoch--,
    dep: --name of the department where the event occurred (optional)--,
      x: --x coordinate of location sensor that fired--,
      y: --y coordinate of location sensor that fired--,
    """
    id: int
    ts: int
    dep: Optional[str]
    x: Optional[int]
    y: Optional[int]


class CustomerEventExtended(BaseModel):
    customer: CustomerDescription
    timestamp: int
    department: Optional[str]
    location: Optional[Location]
    event_type: str
