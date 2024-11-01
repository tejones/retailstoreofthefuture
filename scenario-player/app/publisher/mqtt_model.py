from pydantic import BaseModel, Field


class CustomerEnterEvent(BaseModel):
    """
    Object representing the event of customer entering the store.
    """
    id: str = Field(description='ID representing customer')
    ts: int = Field(description='timestamp of the entrance, in seconds since epoch')


class CustomerExitEvent(BaseModel):
    """
    id: --ID representing customer--,
    ts: --timestamp of the exit, in seconds since epoch--
    """
    id: str
    ts: int


class CustomerMoveEvent(BaseModel):
    """
    id: --ID representing customer--,
    ts: --timestamp of the move, in seconds since epoch--,
     x: --x coordinate of location sensor that fired--,
     y: --y coordinate of location sensor that fired--
    """
    id: str
    ts: int
    x: int
    y: int
