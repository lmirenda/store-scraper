from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, Session, SQLModel

DATABASE_URL = "postgresql://user:password@0.0.0.0:5432/store-scraper-db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    try:
        with Session(engine) as session:
            yield session
    finally:
        session.close()
