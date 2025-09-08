"""
Конфигурация для LLM провайдеров.
Позволяет легко переключаться между различными LLM сервисами.
"""

from typing import Dict, Any
from app.config import CONFIG


def get_llm_config() -> Dict[str, Any]:
    """
    Возвращает конфигурацию для LLM провайдера.
    
    Returns:
        Dict[str, Any]: Конфигурация LLM
    """
    return {
        "provider": CONFIG.get("LLM_PROVIDER", "gemini"),
        "pool_connections": CONFIG.get("LLM_POOL_CONNECTIONS", 10),
        "pool_maxsize": CONFIG.get("LLM_POOL_MAXSIZE", 50),
        "timeout": CONFIG.get("LLM_TIMEOUT", 10.0),
    }


def get_gemini_config() -> Dict[str, Any]:
    """
    Возвращает специфичную конфигурацию для Gemini.
    
    Returns:
        Dict[str, Any]: Конфигурация Gemini
    """
    return {
        "api_key": CONFIG["API_KEY"],
        "endpoint": CONFIG.get("GEMINI_ENDPOINT", "https://api.proxyapi.ru/google/v1beta/models/gemini-2.0-flash:generateContent"),
        "model": CONFIG.get("GEMINI_MODEL", "gemini-2.0-flash"),
    }


