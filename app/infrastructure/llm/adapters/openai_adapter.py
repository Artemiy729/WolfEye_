"""
Пример адаптера для OpenAI API.
Демонстрирует, как легко добавить поддержку нового LLM провайдера.
"""

from typing import Optional, Dict, Any
from app.infrastructure.llm.llm_client import LLMClient
from app.config import CONFIG

import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


class OpenAIAdapter(LLMClient):
    """
    Реализация LLMClient для работы с OpenAI API.
    Демонстрирует паттерн адаптера для другого провайдера.
    """
    
    def __init__(self, *, pool_connections: int = 10, pool_maxsize: int = 50, timeout: float = 10.0):
        """
        Инициализирует адаптер для работы с OpenAI API.
        
        Args:
            pool_connections: Количество соединений в пуле
            pool_maxsize: Максимальный размер пула соединений
            timeout: Таймаут для запросов
        """
        self._ENDPOINT = "https://api.openai.com/v1/chat/completions"
        self._headers = {
            "Authorization": f"Bearer {CONFIG.get('OPENAI_API_KEY', '')}",
            "Content-Type": "application/json",
        }
        self._timeout = timeout
        self._model = CONFIG.get("OPENAI_MODEL", "gpt-4")

        # Настраиваем сессию с пулом соединений и ретраями
        self._session = requests.Session()

        retries = Retry(
            total=3,
            backoff_factor=0.3,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(["POST"]),
            raise_on_status=False,
            respect_retry_after_header=True,
        )

        adapter = HTTPAdapter(
            pool_connections=pool_connections,
            pool_maxsize=pool_maxsize,
            max_retries=retries,
        )

        self._session.mount("http://", adapter)
        self._session.mount("https://", adapter)
    
    def generate_content(
        self, 
        system_prompt: str, 
        user_text: str, 
        generation_config: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Генерирует контент через OpenAI API.
        
        Args:
            system_prompt: Системный промпт
            user_text: Пользовательский текст
            generation_config: Конфигурация генерации
            
        Returns:
            Optional[str]: Сгенерированный текст или None в случае ошибки
        """
        # Формируем payload для OpenAI API
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ]
        
        payload = {
            "model": self._model,
            "messages": messages,
        }
        
        # Добавляем конфигурацию генерации, если есть
        if generation_config:
            # Адаптируем параметры под OpenAI API
            openai_config = {}
            if "temperature" in generation_config:
                openai_config["temperature"] = generation_config["temperature"]
            if "maxOutputTokens" in generation_config:
                openai_config["max_tokens"] = generation_config["maxOutputTokens"]
            if "topP" in generation_config:
                openai_config["top_p"] = generation_config["topP"]
            
            payload.update(openai_config)

        try:
            resp = self._session.post(
                self._ENDPOINT,
                headers=self._headers,
                json=payload,
                timeout=self._timeout,
            )
            resp.raise_for_status()
        except requests.RequestException:
            return None

        try:
            data = resp.json()
            # OpenAI возвращает ответ в другом формате
            text = data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, Exception):
            return None

        return text
    
    def close(self) -> None:
        """
        Закрывает соединения.
        """
        self._session.close()
    
    def __del__(self):
        """
        Деструктор для автоматического закрытия соединений.
        """
        try:
            self._session.close()
        except Exception:
            pass
