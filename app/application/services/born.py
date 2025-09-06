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
    
    Return:
        баллы (0, 2 или 3)
    """
    
    if born is None:
        
        return 3
    
    if first_work is None:
        return 2
    
    age_at_first_work = first_work.year - born.year
    
    if (first_work.month, first_work.day) < (born.month, born.day):
        age_at_first_work -= 1
    
    if age_at_first_work >= 18:
        return 0  
    else:
        return 2  
