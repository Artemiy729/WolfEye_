# -*- coding: utf-8 -*-

"""
Сервис аутентификации
Связывает JWT токены и работу с пользователями в БД
"""

from sqlalchemy.orm import Session
from typing import Optional, Dict
from app.interfaces.api.v1.schemas.auth import User
from app.infrastructure.db.user_repository import UserModel
from app.infrastructure.security.jwt import (
    create_access_token,
    create_refresh_token,
    verify_token,
    verify_refresh_token
)


class AuthService:
    """Сервис аутентификации"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def authenticate_user(self, login: str, password: str) -> Optional[Dict[str, str]]:
        """
        Аутентификация пользователя по логину и паролю
        Возвращает токены или None
        """
        user = self._authenticate_user_credentials(login, password)
        if not user:
            return None
        
        return {
            "access_token": create_access_token(user),
            "refresh_token": create_refresh_token(user)
        }
    
    def get_user_from_token(self, token: str) -> Optional[User]:
        """
        Получение пользователя из access токена
        """
        # Валидируем токен
        payload = verify_token(token)
        if not payload or not payload.get("sub"):
            return None
        
        # Извлекаем user_id
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        # Получаем пользователя из БД
        return self.get_user_by_id(user_id)
    
    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """
        Обновление access токена по refresh токену
        """
        # Валидируем refresh токен
        payload = verify_refresh_token(refresh_token)
        if not payload or not payload.get("sub"):
            return None
        
        # Извлекаем user_id
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        # Получаем пользователя из БД
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        # Создаем новый access токен
        return create_access_token(user)
    
    # Методы для работы с пользователями в БД (из UserService)
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Получение пользователя по ID"""
        user_model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_model:
            return None
        
        return self._convert_to_pydantic(user_model)
    
    def get_user_by_login(self, login: str) -> Optional[User]:
        """Получение пользователя по логину"""
        user_model = self.db.query(UserModel).filter(UserModel.login == login).first()
        if not user_model:
            return None
        
        return self._convert_to_pydantic(user_model)
    
    def _authenticate_user_credentials(self, login: str, password: str) -> Optional[User]:
        """Аутентификация пользователя (логин + пароль)"""
        from app.infrastructure.db.user_repository import authenticate_user
        return authenticate_user(self.db, login, password)
    
    def _convert_to_pydantic(self, user_model: UserModel) -> User:
        """Конвертация SQLAlchemy модели в Pydantic модель"""
        return User(
            id=user_model.id,
            login=user_model.login,
            password_hash=user_model.password_hash
        )
