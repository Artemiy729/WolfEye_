from app.domain.models import PlaceWork
from typing import List

def analyze_company(companies: List[PlaceWork]) -> float:
    """
    Проверяет количество компаний в резюме и выдает на основе этого балл. 
    Руководствуемся логикой, что если указано две компании, то это скорее всего накрутчик.
    Args:
        companies (List[PlaceWork]): Список компаний.

    Returns:
        float: 1 если указано две компании, 0 иначе.
    """
    
    if len(companies) == 2:
        return 1
    
    return 0