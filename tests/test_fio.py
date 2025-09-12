# python -m pytest tests/test_fio.py -v
# -*- coding: utf-8 -*-

import pytest
from app.application.services.fio import analysis_fio, check_fio
from app.domain.models import FIOResult, NameParts


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
    """Тест нормальных ФИО - должны возвращать низкий коэффициент подозрительности (0)"""
    # Нормальные русские ФИО
    assert check_fio(make_fio("Иванов Иван Иванович")) == 0
    assert check_fio(make_fio("Петров Петр Петрович")) == 0
    assert check_fio(make_fio("Сидоров Сидор Сидорович")) == 0
    

### С отстутсвием какие-либо частей
def test_fio_missing_parts():
    """Тест отсутствующих частей ФИО - должны возвращать 1 балл за отсутствие"""
    # Отсутствует отчество
    result = check_fio(make_fio("Иванов Иван"))
    assert result == 0.2  # 1 балл / 5 = 0.2

### Выдуманные но правильные с точки зрения грамматики
def test_fio_nonexistent_but_correct_full():
    """Несуществующая фамилия, имя, отчество - должно вернуть 6 баллов"""
    result = analysis_fio(make_fio("Джунешвили Джуниор Джуниорович"))
    assert result == FIOResult("222")
    # result = check_fio(make_fio("Джунешвили Джуниор Джуниорович"))
    # assert result == 1.0
def test_fio_nonexistent_but_correct_surname():
    """Несуществующие имя, отчество - должно вернуть 4 балла"""
    result = analysis_fio(make_fio("Ткачёв Сеньер Сеньерович")) ## нужно ли учитывать e| ё
    assert result == FIOResult("022")
    # result = check_fio(make_fio("Ткачев Сеньер Сеньерович"))
    # assert result == 0.8
    
def test_fio_nonexistent_but_correct_name():
    """Тест несуществующих Фамилии, отчества - должны возвращать 4 балла"""
    result = analysis_fio(make_fio("Коленвал Александр Мидлович"))
    assert result == FIOResult("202")
    # result = check_fio(make_fio("Коленвал Александр Мидлович"))
    # assert result == 0.8
def test_fio_nonexistent_but_correct_father_name():
    """Тест несуществующих но лексически правильных ФИО - должны возвращать 4 балла"""
    result = analysis_fio(make_fio("Джунешвили Миддл Александрович"))
    assert result == FIOResult("220")
    # result = check_fio(make_fio("Джунешвили Миддл Александрович"))
    # assert result == 0.8
    
### С опечатками    
def test_fio_typos_and_transliteration():
    """Тест опечаток и транслитерации - должны возвращать 4 балла"""
    # Опечатки в реальных ФИО
    result = check_fio(make_fio("Иванов Ивaн Иванович"))  # латинская 'a'
    assert result > 0.6  # 4 балла / 5 = 0.8
    
    result = check_fio(make_fio("Петрoв Петр Петрович"))  # латинская 'o'
    assert result > 0.6


# -----------------------
# Тесты исключения LLM (нет отчества + транслитерация)
# -----------------------

def test_skip_llm_no_fathername_with_translit():
    """Тест пропуска LLM когда нет отчества и есть транслитерация"""
    # Нет отчества + транслитерация в фамилии
    result = check_fio(make_fio("Ivanov Иван"))
    assert result == 1.0  # 4 + 0 + 1 = 5, 5/5 = 1.0
    
    # Нет отчества + транслитерация в имени
    result = check_fio(make_fio("Иванов Ivan"))
    assert result == 1.0  # 0 + 4 + 1 = 5, 5/5 = 1.0
    
    # Нет отчества + транслитерация в обеих частях
    result = check_fio(make_fio("Ivanov Ivan"))
    assert result == 1.0  # 4 + 4 + 1 = 9, min(9/5, 1.0) = 1.0


def test_skip_llm_with_fathername():
    
    # Есть отчество + транслитерация - не должен идти в LLM  4 + 0 + 0 = 0.8
    result = check_fio(make_fio("Ivanov Иван Иванович"))
    
    assert result == 0.8


def test_use_llm_no_translit():
    """Тест использования LLM когда нет транслитерации (даже без отчества)"""
    # Нет отчества + нет транслитерации - должен идти в LLM
    result = check_fio(make_fio("Иванов Иван"))
    
    assert result == 0.2


# -----------------------
# Тесты визуальной подмены (транслиттерации) (все части)
# -----------------------

def test_visual_substitution_all_parts():
    """Тест когда все части имеют визуальную подмену - должен возвращать 444"""
    result = check_fio(make_fio("Ивaнов Ивaн Ивaнович"))  # все с латинскими буквами
    assert result == 1.0  # 4 + 4 + 4 = 12, min(12/5, 1.0) = 1.0


def test_visual_substitution_partial():
    """Тест частичной визуальной подмены"""
    # Только фамилия с подменой
    result = check_fio(make_fio("Ивaнов Иван Иванович"))
    assert result > 0.6  # 4 + 0 + 0 = 4, 4/5 = 0.8
    
    




