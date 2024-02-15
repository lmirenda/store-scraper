from fastapi import FastAPI

from app.schemas.product import Product
from app.scrapers.tata.demo import perform_search
from app.scrapers.tiendainglesa.client import perform_search_async

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/products", response_model=list[Product])
async def get_products(name: str = None, page: int = 1, limit: int = 10) -> list:
    tata_products = perform_search(name)
    return tata_products
