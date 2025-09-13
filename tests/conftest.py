# -*- coding: utf-8 -*-

import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.db.base import Base, get_db
from app.infrastructure.db.user_repository import UserModel
from app.infrastructure.utils.password import get_password_hash


# Тестовая база данных PostgreSQL
# Используем отдельную тестовую БД или добавляем суффикс к основной
TEST_DB_URL = os.getenv("TEST_DB_URL") or os.getenv("DB_URL", "").replace("/wolfeye", "/wolfeye_test")

if not TEST_DB_URL:
    raise ValueError("Необходимо указать TEST_DB_URL или DB_URL в переменных окружения")

engine = create_engine(TEST_DB_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Фикстура для тестовой сессии БД"""
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    
    # Создаем сессию
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Удаляем таблицы после теста
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_user(db_session):
    """Фикстура для тестового пользователя"""
    user = UserModel(
        id="test-user-id",
        login="testuser",
        password_hash=get_password_hash("testpassword")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_users(db_session):
    """Фикстура для нескольких тестовых пользователей"""
    users = [
        UserModel(
            id="user1",
            login="user1",
            password_hash=get_password_hash("password1")
        ),
        UserModel(
            id="user2", 
            login="user2",
            password_hash=get_password_hash("password2")
        ),
        UserModel(
            id="user3",
            login="user3",
            password_hash=get_password_hash("password3")
        )
    ]
    
    for user in users:
        db_session.add(user)
    db_session.commit()
    
    for user in users:
        db_session.refresh(user)
    
    return users


# Переопределяем зависимость get_db для тестов
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Применяем переопределение
from app.infrastructure.db import base
base.get_db = override_get_db
