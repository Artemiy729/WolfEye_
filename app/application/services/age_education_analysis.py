from datetime import date
from app.domain.models import Education, EducationEntry
from app.application.services.higher import analyze_education
from app.application.services.city import compare_cities


def analyze_age_education_comprehensive(
    born: date | None,
    first_work: date | None,
    education: Education,
    residence_city: str
) -> float:
    """
    Комплексный анализ возраста, образования и стажа работы.
    
    Логика:
    1. Дата рождения (возраст и стаж работы):
    - Указан возраст?
        - Да, Работал после 18? да = 0, нет = +2
        - Нет = +3
    
    2. Образование (может быть несколько):
    - Одно
    - Если несколько, берём первое
    - Начало = сентябрь (окончание - 4) года. Работать начал раньше?
        - Да = +2 (считать только, если нет возраста)
        - Нет
        - с первого курса = -1,5
        - со второго = -2
        - с третьего и позже = -3
    
    Интерпретация: сумма / 5 (диапазон 0-1)
    
    Args:
        born: Дата рождения
        first_work: Дата начала первой работы
        education: Данные об образовании
        residence_city: Город проживания
    
    Returns:
        float: Коэффициент подозрительности от 0.0 до 1.0
    """
    
    # 1. Анализ возраста и стажа работы
    born_score = when_start_working(born, first_work, None)
    
    # 2. Анализ образования
    education_score = analyze_education(education, residence_city)
    
    # 3. Дополнительная логика для образования
    education_bonus = _calculate_education_bonus(born, first_work, education)
    
    # 4. Суммируем все баллы
    total_score = born_score + education_score + education_bonus
    
    # 5. Интерпретация: сумма / 5 (диапазон 0-1)
    return max(0.0, min(1.0, total_score / 5.0))


def when_start_working(born: date | None, first_work: date | None, end_university: date | None) -> int:
    """
    Анализирует возраст и дату начала работы.
    
    Логика:
    - Указан возраст?
        - Да, Работал после 18?
            - да = 0
            - нет = +2
        - Нет = +3
    
    Args:
        born: Дата рождения
        first_work: Дата начала первой работы
        end_university: Дата окончания университета (не используется в текущей логике)
    
    Returns:
        int: Штрафные баллы (0, 2 или 3)
    """
    
    # Проверяем, указан ли возраст (дата рождения)
    if born is None:
        return 3
    
    # Возраст указан, проверяем дату начала работы
    if first_work is None:
        return 2
    
    # Вычисляем возраст на момент начала работы
    age_at_first_work = first_work.year - born.year
    
    # Учитываем месяц и день для более точного расчета
    if (first_work.month, first_work.day) < (born.month, born.day):
        age_at_first_work -= 1
    
    # Проверяем, работал ли после 18 лет
    if age_at_first_work >= 18:
        return 0  
    else:
        return 2  


def _calculate_education_bonus(
    born: date | None,
    first_work: date | None,
    education: Education
) -> float:
    """
    Рассчитывает дополнительные баллы на основе связи образования и работы.
    
    Логика:
    - Начало = сентябрь (окончание - 4) года. Работать начал раньше?
    - Да = +2 (считать только, если нет возраста)
    - Нет
        - с первого курса = -1,5
        - со второго = -2
        - с третьего и позже = -3
    
    Args:
        born: Дата рождения
        first_work: Дата начала первой работы
        education: Данные об образовании
    
    Returns:
        float: Дополнительные баллы
    """
    
    # Если нет данных об образовании или работе, возвращаем 0
    if not education or not education.items or first_work is None:
        return 0.0
    
    # Берем первое (основное) образование
    edu_entry = education.items[0]
    
    # Если нет даты окончания образования, возвращаем 0
    if edu_entry.end_date is None:
        return 0.0
    
    # Вычисляем предполагаемую дату начала обучения
    # Начало = сентябрь (окончание - 4) года
    education_start_year = edu_entry.end_date.year - 4
    education_start = date(education_start_year, 9, 1)  # 1 сентября
    
    # Проверяем, начал ли работать раньше начала обучения
    if first_work < education_start:
        # Работать начал раньше обучения
        # Считать только, если нет возраста (born is None)
        if born is None:
            return 2.0
        else:
            return 0.0
    
    # Работать начал после или во время обучения
    # Определяем, с какого курса начал работать
    
    # Вычисляем количество лет между началом обучения и началом работы
    years_diff = first_work.year - education_start.year
    
    # Учитываем месяц для более точного расчета
    if first_work.month < 9:  # до сентября
        years_diff -= 1
    
    # Дополнительная проверка: если работа началась до сентября первого года обучения,
    # считаем как работу с первого курса
    if first_work.year == education_start.year and first_work.month < 9:
        years_diff = 0
    
    # Определяем курс
    if years_diff <= 0:
        # С первого курса
        return -1.5
    elif years_diff == 1:
        # Со второго курса
        return -2.0
    else:
        # С третьего курса и позже
        return -3.0


def _is_education_basic_complete(edu_entry: EducationEntry) -> bool:
    """
    Проверяет базовую полноту данных об образовании (без даты окончания).
    
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


def _is_education_finished(edu_entry: EducationEntry) -> bool:
    """
    Проверяет, окончено ли образование.
    
    ИСПРАВЛЕНИЕ БАГА: образование считается оконченным, если дата окончания <= сегодня
    
    Args:
        edu_entry: Запись об образовании для проверки
    
    Returns:
        bool: True если образование окончено, False иначе
    """
    if edu_entry.end_date is None:
        return False
    
    # ИСПРАВЛЕНИЕ: используем <= вместо < для включения сегодняшней даты
    return edu_entry.end_date <= date.today()


