from app.domain.models import NameParts
from app.infrastructure.llm.llm import LLM

# Исправление: раньше ожидался FIOResult, а по факту на вход приходит ФИО из резюме.
def analysis_fio(llm: LLM, data: NameParts) -> int:
    # Мок: возвращаем 1
    return 1
