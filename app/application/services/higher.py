from app.domain.models import Education, EducationEntry


def analyze_education(education: Education, residence_city: str) -> int:
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
        float: Вероятность
    """
    
    # Проверяем, есть ли данные об образовании
    if not education or not education.items:
        return 1  # Нет данных об образовании
    
    # Берем первое (основное) образование
    edu_entry = education.items[0]
    
    # Проверяем базовую полноту заполнения (университет, город, факультет)
    if not _is_education_basic_complete(edu_entry):
        return 1  # Базовые данные не заполнены
    
    # Проверяем, окончено ли образование
    if not _is_education_finished(edu_entry):
        # Образование не окончено, проверяем совпадение городов
        if not _cities_match(residence_city, edu_entry.city):
            return 0.75  # Не окончено и город не совпадает с проживанием
    
    return 0  


def _is_education_basic_complete(edu_entry: EducationEntry) -> bool:
    """
    Проверяет базовую полноту данных об образовании (без даты окончания).
    
    Проверяет наличие:
    - университет
    - город
    - факультет/специальность
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
    """
    return (
        _is_education_basic_complete(edu_entry) and
        edu_entry.end_date is not None
    )


def _is_education_finished(edu_entry: EducationEntry) -> bool:
    """
    Проверяет, окончено ли образование.
    
    Считается оконченным, если указана дата окончания и она в прошлом.
    """
    if edu_entry.end_date is None:
        return False
    
    from datetime import date
    return edu_entry.end_date < date.today()


def _cities_match(residence_city: str, education_city: str) -> bool:
    """
    Проверяет, совпадают ли города проживания и обучения.
    
    Сравнение происходит без учета регистра и лишних пробелов.
    """
    if not residence_city or not education_city:
        return False
    
    residence_clean = residence_city.strip().lower()
    education_clean = education_city.strip().lower()
    
    return residence_clean == education_clean
