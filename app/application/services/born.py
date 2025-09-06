from datetime import date

def when_start_working(born: date|None, first_work: date|None, end_university: date|None) -> int:
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
