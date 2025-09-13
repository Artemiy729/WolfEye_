# python -m pytest tests/database/test_user_repository.py -v
# -*- coding: utf-8 -*-

import pytest
from sqlalchemy.orm import Session

from app.infrastructure.db.user_repository import get_user_by_login, authenticate_user, UserModel
from app.interfaces.api.v1.schemas.auth import User


class TestUserRepository:
    """Тесты для репозитория пользователей"""
    
    def test_get_user_by_login_exists(self, db_session: Session, test_user: UserModel):
        """Тест получения существующего пользователя по логину"""
        user = get_user_by_login(db_session, "testuser")
        
        assert user is not None
        assert user.id == "test-user-id"
        assert user.login == "testuser"
        assert user.password_hash is not None
    
    def test_get_user_by_login_not_exists(self, db_session: Session):
        """Тест получения несуществующего пользователя по логину"""
        user = get_user_by_login(db_session, "nonexistent")
        
        assert user is None
    
    def test_get_user_by_login_empty_login(self, db_session: Session):
        """Тест получения пользователя с пустым логином"""
        user = get_user_by_login(db_session, "")
        
        assert user is None
    
    def test_get_user_by_login_none_login(self, db_session: Session):
        """Тест получения пользователя с None логином"""
        user = get_user_by_login(db_session, None)
        
        assert user is None
    
    def test_authenticate_user_correct_credentials(self, db_session: Session, test_user: UserModel):
        """Тест аутентификации с правильными учетными данными"""
        user = authenticate_user(db_session, "testuser", "testpassword")
        
        assert user is not None
        assert user.id == "test-user-id"
        assert user.login == "testuser"
    
    def test_authenticate_user_wrong_password(self, db_session: Session, test_user: UserModel):
        """Тест аутентификации с неправильным паролем"""
        user = authenticate_user(db_session, "testuser", "wrongpassword")
        
        assert user is None
    
    def test_authenticate_user_wrong_login(self, db_session: Session, test_user: UserModel):
        """Тест аутентификации с неправильным логином"""
        user = authenticate_user(db_session, "wronguser", "testpassword")
        
        assert user is None
    
    def test_authenticate_user_empty_credentials(self, db_session: Session, test_user: UserModel):
        """Тест аутентификации с пустыми учетными данными"""
        # Пустой логин
        user = authenticate_user(db_session, "", "testpassword")
        assert user is None
        
        # Пустой пароль
        user = authenticate_user(db_session, "testuser", "")
        assert user is None
        
        # Оба пустые
        user = authenticate_user(db_session, "", "")
        assert user is None
    
    def test_authenticate_user_none_credentials(self, db_session: Session, test_user: UserModel):
        """Тест аутентификации с None учетными данными"""
        # None логин
        user = authenticate_user(db_session, None, "testpassword")
        assert user is None
        
        # None пароль
        user = authenticate_user(db_session, "testuser", None)
        assert user is None
        
        # Оба None
        user = authenticate_user(db_session, None, None)
        assert user is None
    
    def test_authenticate_user_case_sensitive(self, db_session: Session, test_user: UserModel):
        """Тест аутентификации с учетом регистра"""
        # Логин в верхнем регистре
        user = authenticate_user(db_session, "TESTUSER", "testpassword")
        assert user is None
        
        # Логин в смешанном регистре
        user = authenticate_user(db_session, "TestUser", "testpassword")
        assert user is None
    
    def test_authenticate_user_special_characters(self, db_session: Session):
        """Тест аутентификации с особыми символами в логине"""
        from app.infrastructure.utils.password import get_password_hash
        
        # Создаем пользователя с особыми символами
        password = "testpassword"
        password_hash = get_password_hash(password)
        
        special_user = UserModel(
            id="special-user",
            login="user@domain.com",
            password_hash=password_hash
        )
        db_session.add(special_user)
        db_session.commit()
        
        # Тестируем аутентификацию с правильным паролем
        user = authenticate_user(db_session, "user@domain.com", password)
        assert user is not None
        assert user.login == "user@domain.com"
        
        # Тестируем с неправильным паролем
        user = authenticate_user(db_session, "user@domain.com", "wrongpassword")
        assert user is None
    
    def test_multiple_users_authenticate(self, db_session: Session, test_users):
        """Тест аутентификации нескольких пользователей"""
        # Тестируем каждого пользователя
        for i, test_user in enumerate(test_users, 1):
            user = authenticate_user(db_session, f"user{i}", f"password{i}")
            assert user is not None
            assert user.login == f"user{i}"
        
        # Тестируем неправильные комбинации
        user = authenticate_user(db_session, "user1", "password2")
        assert user is None
        
        user = authenticate_user(db_session, "user2", "password1")
        assert user is None
    
    def test_user_model_creation(self, db_session: Session):
        """Тест создания модели пользователя"""
        user = UserModel(
            id="new-user",
            login="newuser",
            password_hash="hashed_password"
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        assert user.id == "new-user"
        assert user.login == "newuser"
        assert user.password_hash == "hashed_password"
    
    def test_user_model_unique_constraints(self, db_session: Session):
        """Тест уникальных ограничений модели пользователя"""
        # Создаем первого пользователя
        user1 = UserModel(
            id="user1",
            login="unique_login",
            password_hash="hash1"
        )
        db_session.add(user1)
        db_session.commit()
        
        # Пытаемся создать пользователя с тем же логином
        user2 = UserModel(
            id="user2",
            login="unique_login",  # Дубликат логина
            password_hash="hash2"
        )
        db_session.add(user2)
        
        # Должно возникнуть исключение при коммите
        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()
        
        db_session.rollback()
        

