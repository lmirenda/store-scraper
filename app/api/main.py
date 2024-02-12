from fastapi import FastAPI

from app.schemas.product import Product
from app.scrapers.tiendainglesa.demo import perform_search

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/products", response_model=list[Product])
async def get_products(name: str = None, page: int = 1, limit: int = 10) -> list:
    return perform_search(name)
