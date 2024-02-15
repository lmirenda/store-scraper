from fastapi import FastAPI, Depends

from app.repositories.product import ProductRepository
from app.schemas.product import Product

app = FastAPI()


@app.get("/healthcheck")
def read_root():
    return {"Status": "Online"}


@app.get("/products", response_model=list[Product])
async def get_products(
    repository: ProductRepository = Depends(ProductRepository),
    name: str = None,
    page: int = 1,
    limit: int = 10,
) -> list[Product]:
    products = await repository.get_by_name(name)
    return products
