from app.domain.models import FIOResult, NameParts
from app.infrastructure.llm import get_llm


def calculate_suspicion_score(fio_result: FIOResult) -> float:
    """
    Рассчитывает коэффициент подозрительности ФИО.
    
    Args:
        fio_result: Результат анализа ФИО
        
    Returns:
        float: Коэффициент подозрительности от 0.0 до 1.0
    """
    s = fio_result.surname + fio_result.name + fio_result.father_name
    return min(1.0, s / 5.0)


def analysis_fio(data: NameParts) -> FIOResult:
    """
    Анализирует ФИО с помощью LLM.
    
    Args:
        data: Данные ФИО для анализа
        
    Returns:
        FIOResult: Результат анализа ФИО
    """
    llm = get_llm()
    return llm.checking_FIO(data)
