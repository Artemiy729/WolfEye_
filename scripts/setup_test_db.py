#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для настройки тестовой БД PostgreSQL
"""

import os
import sys
from sqlalchemy import create_engine, text
from app.infrastructure.db.base import Base


def create_test_database():
    """Создание тестовой БД"""
    # Получаем URL основной БД
    main_db_url = os.getenv("DB_URL")
    if not main_db_url:
        print("DB_URL не найден в переменных окружения")
        return False
    
    # Создаем URL для тестовой БД
    test_db_name = "wolfeye_test"
    if "/wolfeye" in main_db_url:
        test_db_url = main_db_url.replace("/wolfeye", f"/{test_db_name}")
    else:
        # Если БД не указана в URL, добавляем её
        test_db_url = main_db_url.rstrip("/") + f"/{test_db_name}"
    
    # URL для подключения к postgres (без указания конкретной БД)
    postgres_url = main_db_url.rsplit("/", 1)[0] + "/postgres"
    
    try:
        # Подключаемся к postgres для создания БД
        postgres_engine = create_engine(postgres_url)
        
        with postgres_engine.connect() as conn:
            # Проверяем, существует ли БД
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{test_db_name}'"))
            if result.fetchone():
                print(f"Тестовая БД '{test_db_name}' уже существует")
            else:
                # Создаем БД
                conn.execute(text(f"CREATE DATABASE {test_db_name}"))
                print(f"Тестовая БД '{test_db_name}' создана")
        
        # Создаем таблицы в тестовой БД
        test_engine = create_engine(test_db_url)
        Base.metadata.create_all(bind=test_engine)
        print("Тестовые таблицы созданы")
        
        # Сохраняем URL тестовой БД в переменную окружения
        os.environ["TEST_DB_URL"] = test_db_url
        print(f"TEST_DB_URL установлен: {test_db_url}")
        
        return True
        
    except Exception as e:
        print(f"Ошибка при создании тестовой БД: {e}")
        return False


def drop_test_database():
    """Удаление тестовой БД"""
    main_db_url = os.getenv("DB_URL")
    if not main_db_url:
        print("DB_URL не найден в переменных окружения")
        return False
    
    test_db_name = "wolfeye_test"
    postgres_url = main_db_url.rsplit("/", 1)[0] + "/postgres"
    
    try:
        postgres_engine = create_engine(postgres_url)
        
        with postgres_engine.connect() as conn:
            # Проверяем, существует ли БД
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{test_db_name}'"))
            if result.fetchone():
                # Удаляем БД
                conn.execute(text(f"DROP DATABASE {test_db_name}"))
                print(f"Тестовая БД '{test_db_name}' удалена")
            else:
                print(f"Тестовая БД '{test_db_name}' не существует")
        
        return True
        
    except Exception as e:
        print(f"Ошибка при удалении тестовой БД: {e}")
        return False


def main():
    """Основная функция"""
    if len(sys.argv) > 1 and sys.argv[1] == "drop":
        success = drop_test_database()
    else:
        success = create_test_database()
    
    if success:
        print("\nНастройка тестовой БД завершена!")
        print("\nТеперь можно запускать тесты:")
        print("python -m pytest tests/test_config.py -v")
        print("python -m pytest tests/ -v")
    else:
        print("\nНастройка тестовой БД не удалась!")
        sys.exit(1)


if __name__ == "__main__":
    main()
