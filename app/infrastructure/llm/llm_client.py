from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class LLMClient(ABC):
    """
    Абстрактный интерфейс для работы с различными LLM провайдерами.
    Определяет контракт для всех реализаций LLM клиентов.
    """
    
    @abstractmethod
    def generate_content(
        self, 
        system_prompt: str, 
        user_text: str, 
        generation_config: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Генерирует контент на основе системного промпта и пользовательского текста.
        
        Args:
            system_prompt: Системный промпт для настройки поведения модели
            user_text: Пользовательский текст для обработки
            generation_config: Конфигурация генерации (температура, токены и т.д.)
            
        Returns:
            Optional[str]: Сгенерированный текст или None в случае ошибки
        """
        pass
    
    @abstractmethod
    def close(self) -> None:
        """
        Закрывает соединения и освобождает ресурсы.
        """
        pass
    
    def __enter__(self):
        """Поддержка контекстного менеджера."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Автоматическое закрытие при выходе из контекста."""
        self.close()
