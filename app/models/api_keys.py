import uuid

from sqlmodel import SQLModel, Field


class ApiKeyModel(SQLModel, table=True):
    __tablename__ = "api_keys"
    api_key: uuid.UUID = Field(primary_key=True, index=True, default_factory=uuid.uuid4)
    active: bool = Field(default=True)
