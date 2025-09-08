from app.domain.models import FIOResult, NameParts
from app.infrastructure.llm import get_llm





def _calculate_suspicion_score(fio_result: FIOResult) -> float:
    """
    Рассчитывает коэффициент подозрительности ФИО.
    
    Args:
        fio_result: Результат анализа ФИО
        
    Returns:
        float: Коэффициент подозрительности от 0.0 до 1.0
    """
    s = fio_result.surname + fio_result.name + fio_result.father_name
    return min(1.0, s / 5.0)


def _has_visual_substitution(name: str) -> bool:
    """Проверяет, есть ли хотя бы одна визуальная подмена в строке"""
    suspicious_chars = 'aoepcyxABEKMHOPCTYX'

    return any(char in suspicious_chars for char in name)


def _analysis_fio(data: NameParts) -> FIOResult:
    """
    Анализирует ФИО с помощью LLM.
    
    Args:
        data: Данные ФИО для анализа
        
    Returns:
        FIOResult: Результат анализа ФИО
    """
    # Проверяем каждую часть отдельно на визуальную подмену
    surname_has_substitution = _has_visual_substitution(data.surname)
    name_has_substitution = _has_visual_substitution(data.name)
    father_name_has_substitution = _has_visual_substitution(data.father_name)
    
    if (surname_has_substitution and name_has_substitution and father_name_has_substitution):
        return FIOResult("444")
    

    llm = get_llm()

    final_result = llm.checking_FIO(data)
    surname_result = final_result.surname
    name_result = final_result.name
    father_name_result = final_result.father_name
    
    if (surname_has_substitution):
        surname_result = 4
    if (name_has_substitution):
        name_result = 4
    if (father_name_has_substitution):
        father_name_result = 4
    return FIOResult(str(surname_result) + str(name_result) + str(father_name_result))


def check_fio(data: NameParts) -> float:
    fio_result = _analysis_fio(data)
    return _calculate_suspicion_score(fio_result)


if __name__ == "__main__":
    print(check_fio(NameParts(surname="Лызь", name="Дмитрий", father_name="Михайлович")))