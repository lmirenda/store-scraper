from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, Session, SQLModel

from migrations.env import DATABASE_URL

connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    try:
        with Session(engine) as session:
            yield session
    finally:
        session.close()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
