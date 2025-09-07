# python -m pytest tests/test_fio.py -v
# -*- coding: utf-8 -*-

import pytest
from app.application.services.fio import check_fio
from app.domain.models import NameParts


def make_fio(fio_string: str) -> NameParts:
    """
    Удобный конструктор NameParts из строки.
    
    Args:
        fio_string: Строка вида "Фамилия Имя Отчество" или "Фамилия Имя"
        
    Returns:
        NameParts: Объект с разобранными частями ФИО
    """
    parts = fio_string.strip().split()
    if len(parts) == 2:
        return NameParts(surname=parts[0], name=parts[1], father_name="")
    elif len(parts) == 3:
        return NameParts(surname=parts[0], name=parts[1], father_name=parts[2])
    else:
        raise ValueError(f"Ожидается 2 или 3 части ФИО, получено {len(parts)}: {fio_string}")


# -----------------------
# Тесты check_fio
# -----------------------

def test_check_fio_normal_names():
    """Тест нормальных ФИО - должны возвращать низкий коэффициент подозрительности"""
    # Нормальные русские ФИО
    assert check_fio(make_fio("Иванов Иван Иванович")) < 0.2
    assert check_fio(make_fio("Петров Петр Петрович")) < 0.2
    assert check_fio(make_fio("Сидоров Сидор Сидорович")) < 0.2


