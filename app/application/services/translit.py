def has_visual_substitution(name: str) -> bool:
    """Проверяет, есть ли хотя бы одна визуальная подмена в строке"""
    suspicious_chars = 'aoepcyxABEKMHOPCTYX'

    return any(char in suspicious_chars for char in name)