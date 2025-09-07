from datetime import date
from app.domain.models import Education


def analyze_age_education_comprehensive(
    born: date | None,
    first_work: date | None,
    education: Education
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
    
    Returns:
        float: Коэффициент подозрительности от 0.0 до 1.0
    """
    
    # 1. Анализ возраста и стажа работы
    born_score = _when_start_working(born, first_work)

    
    # 2. Дополнительная логика для образования
    education_bonus = _calculate_education_bonus(born, first_work, education)
    
    # 3. Суммируем все баллы
    total_score = born_score + education_bonus
    
    # 4. Интерпретация: сумма / 5 (диапазон 0-1)
    return max(0.0, min(1.0, total_score / 5.0))


def _when_start_working(born: date | None, first_work: date | None) -> int:
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
    
    Returns:
        int: Штрафные баллы (0, 2 или 3)
    """
    
    # Проверяем, указан ли возраст (дата рождения)
    if born is None:
        return 3
    
    # Если нет данных о первой работе, считаем как подозрительное
    if first_work is None:
        return 2
    
    # Вычисляем возраст на момент начала работы
    # Обрабатываем високосные годы
    try:
        age_at_work = date(born.year+18, born.month, born.day)
    except ValueError:
        # Если 29 февраля в невисокосном году, используем 28 февраля
        age_at_work = date(born.year+18, born.month, 28)
    
    # Корректируем возраст с учетом месяца
    if age_at_work > first_work:
        return 2
    
    return 0 
    


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
        return 2
    
    # Берем первое (основное) образование
    edu_entry = education.items[0]
    
    # Если нет даты окончания образования, возвращаем 0
    if edu_entry.end_date is None:
        return 2
    
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
    
    # Определяем курс
    if years_diff == 0:
        # С первого курса
        return -1.5
    elif years_diff == 1:
        # Со второго курса
        return -2.0
    else:
        # С третьего курса и позже
        return -3.0


