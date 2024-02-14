from pydantic import BaseModel


class Money(BaseModel):
    amount: int
    currency: str
    decimal_places: int
