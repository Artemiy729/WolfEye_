# python -m pytest tests/utils/test_password_utils.py -v
# -*- coding: utf-8 -*-

import pytest
from app.infrastructure.utils.password import verify_password, get_password_hash


class TestPasswordUtils:
    """Тесты для утилит работы с паролями"""
    
    def test_password_hashing(self):
        """Тест хеширования пароля"""
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        # Хеш не должен быть равен исходному паролю
        assert hashed != password
        # Хеш не должен быть пустым
        assert hashed is not None
        # Хеш должен быть строкой
        assert isinstance(hashed, str)
        # Хеш должен быть достаточно длинным (bcrypt обычно 60 символов)
        assert len(hashed) > 50
    
    def test_password_verification_correct(self):
        """Тест проверки правильного пароля"""
        password = "correct_password"
        hashed = get_password_hash(password)
        
        # Правильный пароль должен проходить проверку
        assert verify_password(password, hashed) is True
    
    def test_password_verification_incorrect(self):
        """Тест проверки неправильного пароля"""
        password = "correct_password"
        wrong_password = "wrong_password"
        hashed = get_password_hash(password)
        
        # Неправильный пароль не должен проходить проверку
        assert verify_password(wrong_password, hashed) is False
    
    def test_password_verification_empty_password(self):
        """Тест проверки пустого пароля"""
        password = "test_password"
        hashed = get_password_hash(password)
        
        # Пустой пароль не должен проходить проверку
        assert verify_password("", hashed) is False
    
    def test_password_verification_none_password(self):
        """Тест проверки None пароля"""
        password = "test_password"
        hashed = get_password_hash(password)
        
        # None пароль должен вызывать исключение
        with pytest.raises(TypeError, match="secret must be unicode or bytes, not None"):
            verify_password(None, hashed)
    
    def test_different_passwords_different_hashes(self):
        """Тест что разные пароли дают разные хеши"""
        password1 = "password1"
        password2 = "password2"
        
        hash1 = get_password_hash(password1)
        hash2 = get_password_hash(password2)
        
        # Хеши должны быть разными
        assert hash1 != hash2
    
    def test_same_password_different_hashes(self):
        """Тест что один пароль может давать разные хеши (из-за соли)"""
        password = "same_password"
        
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Хеши могут быть разными из-за соли
        # Но оба должны проходить проверку
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True
    
    def test_special_characters_in_password(self):
        """Тест пароля со специальными символами"""
        password = "!@#$%^&*()_+-=[]{}|;':\",./<>?`~"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
        assert verify_password("wrong", hashed) is False
    
    def test_unicode_password(self):
        """Тест пароля с unicode символами"""
        password = "пароль123абвгд"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
        assert verify_password("wrong", hashed) is False
    
    def test_very_long_password(self):
        """Тест очень длинного пароля"""
        password = "a" * 1000  # 1000 символов
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
        assert verify_password("wrong", hashed) is False
