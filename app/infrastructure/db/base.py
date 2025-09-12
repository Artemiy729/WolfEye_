from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import CONFIG

"""Базовый модуль для работы с базой данных
    Определение Base = declarative_base()
"""


DATABASE_URL = CONFIG.get("DB_URL", "postgresql+psycopg2://user:password@localhost:5432/wolfeye")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
