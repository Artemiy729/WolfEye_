from datetime import date


def compare_cities(city_of_residence: str, city_of_learning: str, end_university: date|None) -> bool:
    """
    Сравнивает города проживания и обучения.
    
    Args:
        city_of_residence: Город проживания
        city_of_learning: Город обучения
        end_university: Дата окончания университета (не используется в текущей реализации)
    
    Return:
        bool: True если города совпадают, False иначе
    """
    # Мок: считаем совпадающими, если строки равны
    return (city_of_residence or "").strip().lower() == (city_of_learning or "").strip().lower()
