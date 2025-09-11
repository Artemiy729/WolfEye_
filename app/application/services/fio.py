from app.domain.models import FIOResult, NameParts
from app.infrastructure.llm import get_llm
from app.application.services.translit import has_visual_substitution




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




def analysis_fio(data: NameParts) -> FIOResult: ## вернуть приватность
    """Анализирует ФИО с помощью LLM.
    Args:
        data: Фамилия, имя, отчество
        
    Returns:
        FIOResult: Итоговые значения (баллы) для каждой части из NameParts
    """
    
    # Проверяем визуальную подмену для каждой части
    surname_sub = has_visual_substitution(data.surname)
    name_sub = has_visual_substitution(data.name)
    father_sub = has_visual_substitution(data.father_name)
    
    # Если все части имеют подмену - сразу возвращаем 444
    if surname_sub and name_sub and father_sub:
        return FIOResult("444")
    
    # Пропускаем LLM если нет отчества и есть подмена в имени/фамилии
    if not data.father_name.strip() and (surname_sub or name_sub):
        surname_result = 4 if surname_sub else 0
        name_result = 4 if name_sub else 0
        return FIOResult(f"{surname_result}{name_result}1")

    
    llm_result = get_llm().checking_FIO(data)
    
    # Применяем визуальную подмену поверх LLM результата
    surname_result = 4 if surname_sub else llm_result.surname
    name_result = 4 if name_sub else llm_result.name
    father_result = 4 if father_sub else llm_result.father_name
    
    return FIOResult(f"{surname_result}{name_result}{father_result}")


def check_fio(data: NameParts) -> float:
    fio_result = analysis_fio(data) ## вернуть приватность
    return _calculate_suspicion_score(fio_result)


if __name__ == "__main__":
    print(check_fio(NameParts(surname="Лызь", name="Дмитрий", father_name="Михайлович")))