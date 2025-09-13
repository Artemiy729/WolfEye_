# -*- coding: utf-8 -*-

import os
import pytest
from sqlalchemy import create_engine, text
from app.infrastructure.db.base import Base


def test_database_connection():
    """Тест подключения к тестовой БД"""
    test_db_url = os.getenv("TEST_DB_URL") or os.getenv("DB_URL", "").replace("/wolfeye", "/wolfeye_test")
    
    if not test_db_url:
        pytest.skip("TEST_DB_URL не настроен")
    
    try:
        engine = create_engine(test_db_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.fetchone()[0] == 1
        print(f"✅ Подключение к тестовой БД успешно: {test_db_url}")
    except Exception as e:
        pytest.fail(f"❌ Не удалось подключиться к тестовой БД: {e}")


def test_create_test_tables():
    """Тест создания тестовых таблиц"""
    test_db_url = os.getenv("TEST_DB_URL") or os.getenv("DB_URL", "").replace("/wolfeye", "/wolfeye_test")
    
    if not test_db_url:
        pytest.skip("TEST_DB_URL не настроен")
    
    try:
        engine = create_engine(test_db_url)
        Base.metadata.create_all(bind=engine)
        print("✅ Тестовые таблицы созданы успешно")
    except Exception as e:
        pytest.fail(f"❌ Не удалось создать тестовые таблицы: {e}")


def test_drop_test_tables():
    """Тест удаления тестовых таблиц"""
    test_db_url = os.getenv("TEST_DB_URL") or os.getenv("DB_URL", "").replace("/wolfeye", "/wolfeye_test")
    
    if not test_db_url:
        pytest.skip("TEST_DB_URL не настроен")
    
    try:
        engine = create_engine(test_db_url)
        Base.metadata.drop_all(bind=engine)
        print("✅ Тестовые таблицы удалены успешно")
    except Exception as e:
        pytest.fail(f"❌ Не удалось удалить тестовые таблицы: {e}")
