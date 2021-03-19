from datetime import datetime

from pydantic import BaseModel, condecimal


class FocusEventPayload(BaseModel):
    customer_id: int
    department_id: int


class FocusEvent(BaseModel):
    event_type = 'focus event'
    event_timestamp: datetime = None
    payload: FocusEventPayload


class EntryEventPayload(BaseModel):
    customer_id: int


class EntryEvent(BaseModel):
    event_type = 'entry event'
    event_timestamp: datetime = None
    payload: EntryEventPayload


class PredictionResultPayload(BaseModel):
    customer_id: int
    coupon_id: int
    prediction: condecimal(ge=0, le=1)


class PredictionResultEvent(BaseModel):
    event_type = 'prediction result'
    event_timestamp: datetime = None
    payload: PredictionResultPayload
