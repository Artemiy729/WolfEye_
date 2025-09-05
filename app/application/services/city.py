from datetime import date

def compare_cities(city_of_residence: str, city_of_learning: str, end_university: date|None) -> bool:
    # Мок: считаем совпадающими, если строки равны
    return (city_of_residence or "").strip().lower() == (city_of_learning or "").strip().lower()
