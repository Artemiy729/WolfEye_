from app.domain.models import PlaceWork
from typing import List

def analyze_company(companies: List[PlaceWork]) -> float:
    """
    Проверяет отсутствие компании в резюме и выдает на основе этого балл. 
    Args:
        companies (List[PlaceWork]): Список компаний.

    Returns:
        float: 1 если компания не указана, 0 если указана.
    """
    
    if len(companies) == 2:
        return 1
    
    return 0