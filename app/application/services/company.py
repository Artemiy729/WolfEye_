from app.domain.models import PlaceWork
from typing import List

def analyze_company(companies: List[PlaceWork]) -> float:
    """
    Проверяет отсутствие компании в резюме и выдает на основе этого балл. 
    Args:
        companies (List[PlaceWork]): Список компаний.

    Returns:
        float: 1 если нет указания компаний, 0 если указана хотя бы одна.
    """
    
    if len(companies) > 0:
        return 0
    
    return 1