# -*- coding: utf-8 -*-

"""
Middleware для аутентификации
Проверяет токены и добавляет информацию о пользователе в request state
"""

from fastapi import Request
from fastapi.security import HTTPBearer
from app.infrastructure.db.base import get_db
from app.infrastructure.services.auth_service import AuthService
from app.interfaces.api.v1.schemas.auth import User


class AuthMiddleware:
    """Middleware для аутентификации"""
    
    def __init__(self):
        self.security = HTTPBearer()
    
    async def __call__(self, request: Request, call_next):
        """
        Обработка запроса с проверкой аутентификации
        """
        # Пропускаем публичные эндпоинты
        if request.url.path in ["/", "/health", "/docs", "/openapi.json", "/redoc", "/auth/login", "/auth/refresh"]:
            response = await call_next(request)
            return response
        
        # Получаем токен из заголовка Authorization
        token = await self._extract_token(request)
        
        if not token:
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header missing"},
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Проверяем токен и получаем пользователя
        user = await self._authenticate_user(token)
        if not user:
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token"},
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Добавляем пользователя в state запроса
        request.state.current_user = user
        request.state.is_authenticated = True
        
        # Продолжаем обработку запроса
        response = await call_next(request)
        return response
    
    async def _extract_token(self, request: Request) -> str | None:
        """Извлечение токена из заголовка Authorization"""
        try:
            authorization: str = request.headers.get("Authorization")
            if not authorization:
                return None
            
            scheme, token = authorization.split(" ", 1)
            if scheme.lower() != "bearer":
                return None
            
            return token
        except (ValueError, AttributeError):
            return None
    
    async def _authenticate_user(self, token: str) -> User | None:
        """Аутентификация пользователя по токену"""
        try:
            # Получаем сессию БД
            db = next(get_db())
            try:
                # Создаем сервис аутентификации
                auth_service = AuthService(db)
                
                # Получаем пользователя из токена
                user = auth_service.get_user_from_token(token)
                return user
            finally:
                db.close()
        except Exception:
            return None


# Глобальный экземпляр middleware
auth_middleware = AuthMiddleware()
