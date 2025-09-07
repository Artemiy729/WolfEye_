from app.domain.models import PlaceWork
from app.infrastructure.llm import LLMService

### Не используется, планируется сделать отдельный модуль для анализа легенды
def analysis_legend(llm: LLMService, data: PlaceWork, patterns: list[str]) -> int:
    # Мок: возвращаем 1
    return 1
