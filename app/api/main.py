from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.db.database import get_session, create_db_and_tables
from app.dependencies.pagination import PaginationQuery
from app.models.api_keys import ApiKeyModel
from app.repositories.product import ProductRepository
from app.schemas.product import Product

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/healthcheck")
def read_root():
    return {"Status": "Online"}


@app.get("/products", response_model=list[Product])
async def get_products(
    repository: ProductRepository = Depends(ProductRepository),
    pagination: PaginationQuery = Depends(PaginationQuery),
    name: str = None,
) -> list[Product]:
    products = await repository.get_by_name(name)
    return products


@app.get("/api-key")
async def create_api_key(db: Session = Depends(get_session)) -> ApiKeyModel:
    api_key_model = ApiKeyModel()
    db.add(api_key_model)
    db.commit()
    db.refresh(api_key_model)
    return api_key_model
