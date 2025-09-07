def compare_cities(residence_city: str, education_city: str) -> bool:
    """
    Проверяет, совпадают ли города проживания и обучения.
    
    Сравнение происходит без учета регистра и лишних пробелов.
    
    Args:
        residence_city: Город проживания
        education_city: Город обучения
    
    
    Returns:
        bool: True если города совпадают, False иначе
    """
    if not residence_city or not education_city:
        return False
    
    residence_clean = residence_city.strip().lower()
    education_clean = education_city.strip().lower()
    
    return residence_clean == education_clean


