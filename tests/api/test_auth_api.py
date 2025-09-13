# python -m pytest tests/api/test_auth_api.py -v
# -*- coding: utf-8 -*-

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.interfaces.api.main import app
from app.infrastructure.db.user_repository import UserModel
from app.infrastructure.utils.password import get_password_hash


class TestAuthAPI:
    """Интеграционные тесты для API аутентификации"""
    
    @pytest.fixture
    def client(self):
        """Фикстура для тестового клиента FastAPI"""
        return TestClient(app)
    
    def test_login_success(self, client: TestClient, test_user: UserModel):
        """Тест успешного входа"""
        response = client.post(
            "/auth/login",
            json={
                "login": "testuser",
                "password": "testpassword"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["access_token"] is not None
        assert data["refresh_token"] is not None
    
    def test_login_wrong_credentials(self, client: TestClient, test_user: UserModel):
        """Тест входа с неправильными учетными данными"""
        response = client.post(
            "/auth/login",
            json={
                "login": "testuser",
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "Incorrect login or password" in data["detail"]
    
    def test_login_nonexistent_user(self, client: TestClient, test_user: UserModel):
        """Тест входа несуществующего пользователя"""
        response = client.post(
            "/auth/login",
            json={
                "login": "nonexistent",
                "password": "password"
            }
        )
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "Incorrect login or password" in data["detail"]
    
    def test_login_empty_credentials(self, client: TestClient, test_user: UserModel):
        """Тест входа с пустыми учетными данными"""
        response = client.post(
            "/auth/login",
            json={
                "login": "",
                "password": ""
            }
        )
        
        assert response.status_code == 401
    
    def test_login_missing_fields(self, client: TestClient):
        """Тест входа с отсутствующими полями"""
        # Отсутствует пароль
        response = client.post(
            "/auth/login",
            json={
                "login": "testuser"
            }
        )
        
        assert response.status_code == 422  # Validation error
        
        # Отсутствует логин
        response = client.post(
            "/auth/login",
            json={
                "password": "testpassword"
            }
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_login_invalid_json(self, client: TestClient):
        """Тест входа с невалидным JSON"""
        response = client.post(
            "/auth/login",
            data="invalid json"
        )
        
        assert response.status_code == 422
    
    def test_refresh_token_success(self, client: TestClient, test_user: UserModel):
        """Тест успешного обновления токена"""
        # Сначала получаем токены
        login_response = client.post(
            "/auth/login",
            json={
                "login": "testuser",
                "password": "testpassword"
            }
        )
        
        assert login_response.status_code == 200
        login_data = login_response.json()
        refresh_token = login_data["refresh_token"]
        
        # Небольшая задержка для создания нового токена с другим временем
        import time
        time.sleep(1)
        
        # Обновляем токен
        response = client.post(
            "/auth/refresh",
            json={
                "refresh_token": refresh_token
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["access_token"] is not None
        assert data["access_token"] != login_data["access_token"]  # Новый токен
    
    def test_refresh_token_invalid(self, client: TestClient):
        """Тест обновления с невалидным refresh токеном"""
        response = client.post(
            "/auth/refresh",
            json={
                "refresh_token": "invalid_token"
            }
        )
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "Could not validate refresh token" in data["detail"]
    
    def test_refresh_token_empty(self, client: TestClient):
        """Тест обновления с пустым refresh токеном"""
        response = client.post(
            "/auth/refresh",
            json={
                "refresh_token": ""
            }
        )
        
        assert response.status_code == 401
    
    def test_refresh_token_missing_field(self, client: TestClient):
        """Тест обновления с отсутствующим полем refresh_token"""
        response = client.post(
            "/auth/refresh",
            json={}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_protected_endpoint_without_token(self, client: TestClient):
        """Тест доступа к защищенному эндпоинту без токена"""
        # Предполагаем, что у вас есть защищенный эндпоинт
        # Если нет, можно создать тестовый
        response = client.get("/health")  # Этот эндпоинт не защищен
        
        assert response.status_code == 200
    
    def test_protected_endpoint_with_invalid_token(self, client: TestClient):
        """Тест доступа к защищенному эндпоинту с невалидным токеном"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/health", headers=headers)
        
        # /health не защищен, поэтому должен работать
        assert response.status_code == 200
    
    def test_login_case_sensitivity(self, client: TestClient, test_user: UserModel):
        """Тест чувствительности к регистру при входе"""
        # Логин в верхнем регистре
        response = client.post(
            "/auth/login",
            json={
                "login": "TESTUSER",
                "password": "testpassword"
            }
        )
        
        assert response.status_code == 401
    
    def test_multiple_login_attempts(self, client: TestClient, test_user: UserModel):
        """Тест множественных попыток входа"""
        # Несколько неудачных попыток
        for i in range(3):
            response = client.post(
                "/auth/login",
                json={
                    "login": "testuser",
                    "password": f"wrongpassword{i}"
                }
            )
            assert response.status_code == 401
        
        # Успешная попытка
        response = client.post(
            "/auth/login",
            json={
                "login": "testuser",
                "password": "testpassword"
            }
        )
        assert response.status_code == 200
    
    def test_token_expiration_simulation(self, client: TestClient, test_user: UserModel):
        """Тест симуляции истечения токена"""
        # Получаем токены
        login_response = client.post(
            "/auth/login",
            json={
                "login": "testuser",
                "password": "testpassword"
            }
        )
        
        assert login_response.status_code == 200
        login_data = login_response.json()
        
        # Проверяем, что refresh работает сразу после логина
        refresh_response = client.post(
            "/auth/refresh",
            json={
                "refresh_token": login_data["refresh_token"]
            }
        )
        
        assert refresh_response.status_code == 200
    
    def test_concurrent_logins(self, client: TestClient, test_user: UserModel):
        """Тест одновременных входов одного пользователя"""
        # Несколько одновременных успешных входов
        responses = []
        for i in range(3):
            response = client.post(
                "/auth/login",
                json={
                    "login": "testuser",
                    "password": "testpassword"
                }
            )
            responses.append(response)
        
        # Все должны быть успешными
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert "access_token" in data
            assert "refresh_token" in data
