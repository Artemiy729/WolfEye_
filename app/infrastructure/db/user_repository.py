import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import Session
from typing import Optional
from .base import Base
from app.interfaces.api.v1.schemas.auth import User
from app.infrastructure.utils.password import verify_password

"""SQLAlchemy-модель UserModel
    CRUD-функции для пользователей (get_user_by_login, create_user, и т.п.)
"""
class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    login = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

def get_user_by_login(db: Session, login: str) -> Optional[User]:
    """Получение пользователя по логину"""
    obj = db.query(UserModel).filter(UserModel.login == login).first()
    if obj:
        return User(id=obj.id, login=obj.login, password_hash=obj.password_hash)
    return None


def authenticate_user(db: Session, login: str, password: str) -> Optional[User]:
    """Аутентификация пользователя"""
    
    # Проверяем что логин и пароль не None и не пустые
    if not login or not password:
        return None
    
    user = get_user_by_login(db, login)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
