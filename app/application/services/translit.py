from WolfEye.app.domain.models import NameParts


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
    return NameParts(surname=fio.surname.replace(suspicious_chars, ''), name=fio.name.replace(suspicious_chars, ''), father_name=fio.father_name.replace(suspicious_chars, ''))