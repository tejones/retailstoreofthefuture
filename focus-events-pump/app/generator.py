from datetime import datetime
from random import choice, randint
from typing import Optional

from pydantic import BaseModel, Field


class FocusEvent(BaseModel):
    customer_id: str = Field(alias='id')
    ts: int
    dep: str
    x: Optional[int]
    y: Optional[int]


class FocusEventGenerator:
    def __init__(self, available_dep_list: list[str], pick_customer_func=None):
        self.available_dep_list = available_dep_list
        if pick_customer_func is None:
            self.pick_customer_func = lambda: randint(1, 997)
        else:
            self.pick_customer_func = pick_customer_func

    def generate(self) -> FocusEvent:
        timestamp = datetime.now().timestamp()
        department = choice(self.available_dep_list)
        customer_id = self.pick_customer_func()

        return FocusEvent(id=customer_id, ts=timestamp, dep=department, x=None, y=None)
