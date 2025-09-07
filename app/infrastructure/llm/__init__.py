from typing import Dict, Any
from .llm_client import LLMClient
from .adapters import GeminiAdapter, OpenAIAdapter
from .prompts.fio import FIO_PROMPT
from app.domain.models import FIOResult, NameParts


class LLMService:
    """
    Сервис для работы с LLM, использующий абстрактный интерфейс LLMClient.
    Содержит бизнес-логику для различных типов анализа.
    """
    
    def __init__(self, llm_client: LLMClient):
        """
        Инициализирует сервис с конкретной реализацией LLMClient.
        
        Args:
            llm_client: Реализация интерфейса LLMClient
        """
        self._llm_client = llm_client
    
    def checking_FIO(self, data: NameParts) -> FIOResult:
        """
        Анализирует ФИО с помощью LLM.
        
        Args:
            data: Данные ФИО для анализа
            
        Returns:
            FIOResult: Результат анализа ФИО
        """
        generation_config = {
            "candidateCount": 1,
            "maxOutputTokens": 3,
            "temperature": 0.0,
            "topP": 1.0,
            "seed": 0,
            "responseMimeType": "text/plain",
        }
        
        response = self._llm_client.generate_content(
            system_prompt=FIO_PROMPT,
            user_text=str(data),
            generation_config=generation_config
        )
        
        if response is None:
            return FIOResult("000")
        return FIOResult(response)

    def analysis_of_legend(self, text: str, patterns: Dict[int, str]) -> int:
        """
        Анализ легенды резюме на предмет накрутки.
        
        Args:
            text: Текст для анализа
            patterns: Паттерны для поиска
            
        Returns:
            int: Результат анализа (пока мок - возвращает 1)
        """
        # Реализовать реальный анализ легенды
        return 1
    
    def close(self) -> None:
        """
        Закрывает соединения LLM клиента.
        """
        self._llm_client.close()


# Фабрика для создания LLM сервиса
def create_llm_service(provider: str = "gemini", **kwargs) -> LLMService:
    """
    Создает LLM сервис с указанным провайдером.
    
    Args:
        provider: Провайдер LLM ("gemini", "openai", etc.)
        **kwargs: Дополнительные параметры для инициализации клиента
        
    Returns:
        LLMService: Настроенный сервис LLM
        
    Raises:
        ValueError: Если указан неподдерживаемый провайдер
    """
    if provider == "gemini":
        llm_client = GeminiAdapter(**kwargs)
    elif provider == "openai": ## на всякий случай как пример пусть будет
        llm_client = OpenAIAdapter(**kwargs)
    else:
        raise ValueError(f"Неподдерживаемый провайдер LLM: {provider}")
    
    return LLMService(llm_client)


# Глобальный экземпляр для обратной совместимости
_llm_service = create_llm_service()


def get_llm() -> LLMService:
    """
    Возвращает глобальный экземпляр LLM сервиса.
    Для обратной совместимости с существующим кодом.
    
    Returns:
        LLMService: Глобальный экземпляр сервиса
    """
    return _llm_service

