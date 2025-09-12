import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import Session
from .base import Base
from app.interfaces.api.v1.schemas.auth import User

"""SQLAlchemy-модель UserModel
    CRUD-функции для пользователей (get_user_by_login, create_user, и т.п.)
"""
class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    login = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

def get_user_by_login(db: Session, login: str) -> User | None:
    obj = db.query(UserModel).filter(UserModel.login == login).first()
    if obj:
        return User(id=obj.id, login=obj.login, email=obj.email, password_hash=obj.password_hash)
    return None
