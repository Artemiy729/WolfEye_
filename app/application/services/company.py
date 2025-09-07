from app.domain.models import PlaceWork


def analyze_company(current_company: PlaceWork) -> float:
    """
    Проверяет отсутствие компании в резюме и выдает на основе этого балл. 
    Args:
        current_company (PlaceWork): Текущая компания.

    Returns:
        float: 1 если компания не указана, 0 если указана.
    """
    
    
    if current_company.company is None:
        return 1
    
    return 0