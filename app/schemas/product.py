from pydantic import BaseModel

from app.schemas.money import Money


class Product(BaseModel):
    name: str
    # description: str | None = None
    regular_price: Money
    discount_price: Money
    redirect_url: str | None = None
    provider: str | None = None
