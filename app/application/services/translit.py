from app.domain.models import NameParts


def has_visual_substitution(name: str) -> bool:
    """Проверяет, есть ли хотя бы одна визуальная подмена в строке"""
    suspicious_chars = 'aoepcyxABEKMHOPCTYX'

    return any(char in suspicious_chars for char in name)


def change_to_normal(fio: NameParts) -> NameParts:
    """Исправляет визуальную подмену.

    Args:
        fio (NameParts): Фамилия, имя, отчество до исправления

    Returns:
        NameParts: Фамилия, имя, отчество после исправления
    """
    suspicious_chars = 'aoepcyxABEKMHOPCTYX'
    suspicious_chars_dict = {
        'a': 'а',
        'o': 'о',
        'e': 'е',
        'p': 'р',
        'c': 'с',
        'y': 'у',
        'x': 'х',
        'A': 'А',
        'B': 'В',
        'E': 'Е',
        'K': 'К',
        'M': 'М',
        'H': 'Н',
        'O': 'О',
        'P': 'Р',
        'C': 'С',
        'T': 'Т',
        'Y': 'У',
        'X': 'Х',
    }
    for char in suspicious_chars:
        fio.surname = fio.surname.replace(char, suspicious_chars_dict[char])
        fio.name = fio.name.replace(char, suspicious_chars_dict[char])
        fio.father_name = fio.father_name.replace(char, suspicious_chars_dict[char])
        
    return fio