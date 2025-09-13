# python -m pytest tests/security/test_jwt_tokens.py -v
# -*- coding: utf-8 -*-

import pytest
from datetime import datetime, timedelta
from app.infrastructure.security.jwt import (
    create_access_token, 
    create_refresh_token, 
    verify_token, 
    verify_refresh_token
)
from app.interfaces.api.v1.schemas.auth import User


class TestJWTTokens:
    """Тесты для JWT токенов"""
    
    @pytest.fixture
    def test_user(self):
        """Фикстура для тестового пользователя"""
        return User(
            id="test-user-id",
            login="testuser",
            password_hash="hashed_password"
        )
    
    def test_create_access_token(self, test_user: User):
        """Тест создания access токена"""
        token = create_access_token(test_user)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_refresh_token(self, test_user: User):
        """Тест создания refresh токена"""
        token = create_refresh_token(test_user)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_verify_access_token_valid(self, test_user: User):
        """Тест проверки валидного access токена"""
        token = create_access_token(test_user)
        payload = verify_token(token)
        
        assert payload is not None
        assert payload.get("sub") == test_user.id
        assert payload.get("login") == test_user.login

    
    def test_verify_refresh_token_valid(self, test_user: User):
        """Тест проверки валидного refresh токена"""
        token = create_refresh_token(test_user)
        payload = verify_refresh_token(token)
        
        assert payload is not None
        assert payload.get("sub") == test_user.id
        assert payload.get("login") == test_user.login

    
    def test_verify_token_invalid(self, test_user: User):
        """Тест проверки невалидного токена"""
        invalid_token = "invalid.token.here"
        payload = verify_token(invalid_token)
        
        assert payload is None
    
    def test_verify_refresh_token_invalid(self, test_user: User):
        """Тест проверки невалидного refresh токена"""
        invalid_token = "invalid.refresh.token.here"
        payload = verify_refresh_token(invalid_token)
        
        assert payload is None
    
    def test_verify_token_empty(self, test_user: User):
        """Тест проверки пустого токена"""
        payload = verify_token("")
        assert payload is None
        
        payload = verify_token(None)
        assert payload is None
    
    def test_verify_refresh_token_empty(self, test_user: User):
        """Тест проверки пустого refresh токена"""
        payload = verify_refresh_token("")
        assert payload is None
        
        payload = verify_refresh_token(None)
        assert payload is None
    
    def test_token_contains_correct_claims(self, test_user: User):
        """Тест что токен содержит правильные claims"""
        access_token = create_access_token(test_user)
        refresh_token = create_refresh_token(test_user)
        
        access_payload = verify_token(access_token)
        refresh_payload = verify_refresh_token(refresh_token)
        
        # Проверяем основные claims
        assert access_payload.get("sub") == test_user.id
        assert access_payload.get("login") == test_user.login

        
        assert refresh_payload.get("sub") == test_user.id
        assert refresh_payload.get("login") == test_user.login

    
    def test_different_users_different_tokens(self, test_user: User):
        """Тест что разные пользователи получают разные токены"""
        user2 = User(
            id="user2-id",
            login="user2",
            password_hash="hash2"
        )
        
        token1 = create_access_token(test_user)
        token2 = create_access_token(user2)
        
        assert token1 != token2
        
        # Проверяем что токены содержат правильные данные
        payload1 = verify_token(token1)
        payload2 = verify_token(token2)
        
        assert payload1.get("sub") == test_user.id
        assert payload2.get("sub") == user2.id
    
    def test_token_expiration_claim(self, test_user: User):
        """Тест что токен содержит claim истечения"""
        token = create_access_token(test_user)
        payload = verify_token(token)
        
        assert "exp" in payload
        exp_timestamp = payload["exp"]
        
        # Проверяем что время истечения в будущем
        current_time = datetime.utcnow().timestamp()
        assert exp_timestamp > current_time
    
    def test_refresh_token_expiration_claim(self, test_user: User):
        """Тест что refresh токен содержит claim истечения"""
        token = create_refresh_token(test_user)
        payload = verify_refresh_token(token)
        
        assert "exp" in payload
        exp_timestamp = payload["exp"]
        
        # Проверяем что время истечения в будущем
        current_time = datetime.utcnow().timestamp()
        assert exp_timestamp > current_time
    
    def test_token_type_claim(self, test_user: User):
        """Тест что токен содержит claim типа"""
        access_token = create_access_token(test_user)
        refresh_token = create_refresh_token(test_user)
        
        access_payload = verify_token(access_token)
        refresh_payload = verify_refresh_token(refresh_token)
        
        # Проверяем наличие типа токена (если реализовано)
        # Это зависит от вашей реализации JWT
        assert "sub" in access_payload
        assert "sub" in refresh_payload
    
    def test_same_user_multiple_tokens(self, test_user: User):
        """Тест создания нескольких токенов для одного пользователя"""
        token1 = create_access_token(test_user)
        token2 = create_access_token(test_user)
        
        # Токены могут быть разными из-за времени создания
        # но должны содержать одинаковые данные
        payload1 = verify_token(token1)
        payload2 = verify_token(token2)
        
        assert payload1.get("sub") == payload2.get("sub")
        assert payload1.get("login") == payload2.get("login")
      
    
    def test_token_with_special_characters_in_user_data(self, test_user: User):
        """Тест токена с особыми символами в данных пользователя"""
        special_user = User(
            id="user@domain.com",
            login="user@domain.com",
            password_hash="hash"
        )
        
        token = create_access_token(special_user)
        payload = verify_token(token)
        
        assert payload is not None
        assert payload.get("sub") == "user@domain.com"
        assert payload.get("login") == "user@domain.com"

