from app.domain.models import PlaceWork
from app.infrastructure.llm import LLM

def analysis_legend(llm: LLM, data: PlaceWork, patterns: list[str]) -> int:
    # Мок: возвращаем 1
    return 1
