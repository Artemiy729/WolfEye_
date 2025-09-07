from app.domain.models import Education, EducationEntry
from app.application.services.city import compare_cities


def analyze_education(education: Education, residence_city: str) -> float:
    """
    Анализирует данные о ВУЗе.
    
    Логика:
    - Должен быть полностью заполнен, иначе 100% баллов
    - Что могут не/фейкового указать:
        - настоящее наименование вуза (тогда не будет города обучения после названия и запятой) (фейк)
        - Кафедру (не)
        - специальность (не) 
        - дату окончания (не)
    - Окончено?
        - Да = 0%
        - Нет и город не совпадает с проживанием = 75%
    
    Args:
        education: Данные об образовании
        residence_city: Город проживания
    
    Returns:
        float: Вероятность подозрительности от 0.0 до 1.0
    """
    
    # Проверяем, есть ли данные об образовании
    if not education or not education.items:
        return 1 
    
    # Берем первое (основное) образование
    edu_entry = education.items[0]
    
    # Проверяем базовую полноту заполнения (университет, город, факультет)
    if not _is_education_basic_complete(edu_entry):
        return 1  # Базовые данные не заполнены
    
    # Проверяем, окончено ли образование
    if not _is_education_finished(edu_entry):
        # Образование не окончено, проверяем совпадение городов
        if not compare_cities(residence_city, edu_entry.city):
            return 0.75  # Не окончено и город не совпадает с проживанием
        else:
            return 0  # Не окончено, но город совпадает с проживанием
    
    return 0  # Образование окончено  


def _is_education_basic_complete(edu_entry: EducationEntry) -> bool:
    """
    Проверяет базовую полноту данных об образовании (без даты окончания).
    
    Проверяет наличие:
    - университет
    - город
    - факультет/специальность
    
    Args:
        edu_entry: Запись об образовании для проверки
    
    Returns:
        bool: True если все базовые поля заполнены, False иначе
    """
    return (
        edu_entry.university is not None and 
        edu_entry.university.strip() != "" and
        edu_entry.city is not None and 
        edu_entry.city.strip() != "" and
        edu_entry.faculty is not None and 
        edu_entry.faculty.strip() != ""
    )


def _is_education_complete(edu_entry: EducationEntry) -> bool:
    """
    Проверяет, полностью ли заполнены данные об образовании.
    
    Проверяет наличие:
    - университет
    - город
    - факультет/специальность
    - дата окончания
    
    Args:
        edu_entry: Запись об образовании для проверки
    
    Returns:
        bool: True если все поля заполнены, False иначе
    """
    return (
        _is_education_basic_complete(edu_entry) and
        edu_entry.end_date is not None
    )


def _is_education_finished(edu_entry: EducationEntry) -> bool:
    """
    Проверяет, окончено ли образование.
    
    Считается оконченным, если указана дата окончания и она в прошлом.
    
    Args:
        edu_entry: Запись об образовании для проверки
    
    Returns:
        bool: True если образование окончено, False иначе
    """
    if edu_entry.end_date is None:
        return False
    
    from datetime import date
    return edu_entry.end_date < date.today()


