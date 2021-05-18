from typing import Optional

from pydantic import BaseModel, Field


class FocusEvent(BaseModel):
    customer_id: str = Field(alias='id')
    ts: int
    dep: str
    x: Optional[int]
    y: Optional[int]


class EntryEvent(BaseModel):
    customer_id: str = Field(alias='id')
    ts: int
