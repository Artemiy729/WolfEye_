from app.domain.models import FIOResult, NameParts
from app.infrastructure.llm import get_llm

# Исправление: раньше ожидался FIOResult, а по факту на вход приходит ФИО из резюме.
def analysis_fio(data: NameParts) -> FIOResult:
    llm = get_llm()
    return llm.checking_FIO(data)
