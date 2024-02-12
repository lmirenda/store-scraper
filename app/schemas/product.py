from pydantic import BaseModel

from app.schemas.money import Money


class Product(BaseModel):
    name: str
    # description: str | None = None
    price: str
    image: str | None = None
    # provider: str | None = None
