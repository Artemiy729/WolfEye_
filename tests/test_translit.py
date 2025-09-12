### Проверка исправления визуальной подмены
from app.application.services.translit import change_to_normal
from tests.test_fio import make_fio


def test_visual_substitution_correction():
    """Тест исправления визуальной подмены"""
    result = change_to_normal(make_fio("Ивaнов Иван Иванович"))
    assert result == make_fio("Иванов Иван Иванович")
def test_visual_substitution_correction_partial():
    """Тест исправления визуальной подмены"""
    result = change_to_normal(make_fio("Ивaнов Иван"))
    assert result == make_fio("Иванов Иван")
def test_visual_substitution_correction_all():
    """Тест исправления визуальной подмены"""
    result = change_to_normal(make_fio("Ивaнов Ивaн Ивaнович"))
    assert result == make_fio("Иванов Иван Иванович")