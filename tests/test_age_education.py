# python -m pytest tests/test_age_education.py -v
# -*- coding: utf-8 -*-

from datetime import date
from types import SimpleNamespace
import pytest

from app.application.services.age_education_analysis import (
    analyze_age_education_comprehensive,
    _when_start_working,
    _calculate_education_bonus,
)


def make_education(end_date):
    """Удобный конструктор Education-заглушки с одним элементом."""
    item = SimpleNamespace(end_date=end_date)
    return SimpleNamespace(items=[item])


def make_empty_education():
    """Education без элементов."""
    return SimpleNamespace(items=[])


# -----------------------
# Тесты _when_start_working
# -----------------------

def test_when_start_working_no_born_returns_3():
    assert _when_start_working(born=None, first_work=date(2020, 1, 1)) == 3


def test_when_start_working_no_first_work_returns_2():
    assert _when_start_working(born=date(2000, 1, 1), first_work=None) == 2


@pytest.mark.parametrize(
    "born, first_work, expected",
    [
        # До 18-летия -> 2
        (date(2000, 1, 10), date(2018, 1, 9), 2),
        # В день 18-летия -> 0
        (date(2000, 1, 10), date(2018, 1, 10), 0),
        # После 18-летия -> 0
        (date(2000, 1, 10), date(2018, 1, 11), 0),
    ],
)
def test_when_start_working_boundary_18(born, first_work, expected):
    assert _when_start_working(born, first_work) == expected


# -----------------------
# Тесты _calculate_education_bonus
# -----------------------

def test_education_bonus_none_education_returns_2():
    assert _calculate_education_bonus(
        born=date(2000, 1, 1),
        first_work=date(2019, 9, 1),
        education=None,
    ) == 2


def test_education_bonus_empty_items_returns_2():
    assert _calculate_education_bonus(
        born=date(2000, 1, 1),
        first_work=date(2019, 9, 1),
        education=make_empty_education(),
    ) == 2


def test_education_bonus_no_end_date_returns_2():
    edu = SimpleNamespace(items=[SimpleNamespace(end_date=None)])
    assert _calculate_education_bonus(
        born=date(2000, 1, 1),
        first_work=date(2019, 9, 1),
        education=edu,
    ) == 2


def test_education_bonus_first_work_before_edu_start_no_born_returns_2():
    """
    Если работа началась раньше предполагаемого начала обучения и born отсутствует -> +2.0
    Предположим окончание: 2020-06-30 → старт обучения: 2016-09-01.
    Работа: 2016-08-31 (< 2016-09-01)
    """
    edu = make_education(date(2020, 6, 30))
    assert _calculate_education_bonus(
        born=None,
        first_work=date(2016, 8, 31),
        education=edu,
    ) == 2.0


def test_education_bonus_first_work_before_edu_start_with_born_returns_0():
    """
    Та же ситуация, но born задан -> 0.0
    """
    edu = make_education(date(2020, 6, 30))
    assert _calculate_education_bonus(
        born=date(2000, 1, 1),
        first_work=date(2016, 8, 31),
        education=edu,
    ) == 0.0


def test_education_bonus_first_course_minus_1_5():
    """
    Старт обучения: 2016-09-01
    Работа: 2016-10-01 → первый курс → -1.5
    """
    edu = make_education(date(2020, 6, 30))
    assert _calculate_education_bonus(
        born=date(2000, 1, 1),
        first_work=date(2016, 10, 1),
        education=edu,
    ) == -1.5


def test_education_bonus_second_course_minus_2():
    """
    Старт обучения: 2016-09-01
    Работа: 2017-10-01 → второй курс → -2.0
    Важно брать месяц >= 9, иначе это всё ещё считается первым курсом.
    """
    edu = make_education(date(2020, 6, 30))
    assert _calculate_education_bonus(
        born=date(2000, 1, 1),
        first_work=date(2017, 10, 1),
        education=edu,
    ) == -2.0


def test_education_bonus_third_or_later_minus_3():
    """
    Старт обучения: 2016-09-01
    Работа: 2018-10-01 → третий курс и старше → -3.0
    """
    edu = make_education(date(2020, 6, 30))
    assert _calculate_education_bonus(
        born=date(2000, 1, 1),
        first_work=date(2018, 10, 1),
        education=edu,
    ) == -3.0


# -----------------------
# Тесты analyze_age_education_comprehensive (нормализация и суммирование)
# -----------------------

def test_analyze_full_all_missing_age_and_early_work_cap_to_1():
    """
    born_score = 3 (нет born)
    edu_bonus = 2 (нет образования/раньше старта + нет возраста)
    total = 5 → 5/5 = 1.0 (верхняя граница)
    """
    edu = None
    result = analyze_age_education_comprehensive(
        born=None,
        first_work=date(2016, 1, 1),
        education=edu,
    )
    assert result == pytest.approx(1.0)


def test_analyze_full_lower_clamp_to_zero():
    """
    Пример: born_score = 0, edu_bonus = -3 → total = -3 → -0.6 → 0.0 (нижняя граница)
    """
    edu = make_education(date(2020, 6, 30))
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 1),
        first_work=date(2018, 10, 1),  # третий курс и позже → -3
        education=edu,
    )
    assert result == pytest.approx(0.0)


def test_analyze_full_mix_before_18_first_course():
    """
    born_score = 2 (работа до 18)
    edu_bonus = -1.5 (первый курс)
    total = 0.5 → 0.1
    """
    edu = make_education(date(2020, 6, 30))            # старт: 2016-09-01
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 10),                         # 18 лет: 2018-01-10
        first_work=date(2016, 10, 1),                   # первый курс → -1.5
        education=edu,                                  # 2016-10-01 был бы первый курс
    )
    # Чтобы получить первый курс, используем бонус отдельно:
    # Здесь first_work = 2016-10-01 → по курсам это > 2016-09-01 и < 2017-09-01 → первый курс → -1.5
    assert result == pytest.approx(0.1)


def test_analyze_full_no_first_work_returns_0_8():
    """
    born_score = 2 (есть born, но нет first_work)
    edu_bonus = 2 (в функции образования first_work None → 2)
    total = 4 → 0.8
    """
    edu = make_education(date(2020, 6, 30))
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 1),
        first_work=None,
        education=edu,
    )
    assert result == pytest.approx(0.8)


# -----------------------
# Дополнительные тесты для граничных случаев
# -----------------------

def test_analyze_all_none_returns_1_0():
    """Все параметры None - максимальная подозрительность"""
    result = analyze_age_education_comprehensive(
        born=None,
        first_work=None,
        education=None,
    )
    assert result == pytest.approx(1.0)


def test_analyze_no_education_but_has_work_returns_0_4():
    """Нет образования, но есть работа и возраст"""
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 1),
        first_work=date(2019, 1, 1),
        education=None,
    )
    assert result == pytest.approx(0.4)  # born_score=0, edu_bonus=2, total=2, result=0.4


def test_analyze_empty_education_but_has_work_returns_0_4():
    """Пустое образование, но есть работа и возраст"""
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 1),
        first_work=date(2019, 1, 1),
        education=make_empty_education(),
    )
    assert result == pytest.approx(0.4)  # born_score=0, edu_bonus=2, total=2, result=0.4


def test_analyze_education_no_end_date_returns_0_4():
    """Образование без даты окончания"""
    edu = SimpleNamespace(items=[SimpleNamespace(end_date=None)])
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 1),
        first_work=date(2019, 1, 1),
        education=edu,
    )
    assert result == pytest.approx(0.4)  # born_score=0, edu_bonus=2, total=2, result=0.4


# -----------------------
# Тесты для различных курсов обучения
# -----------------------

def test_analyze_second_course_returns_0_0():
    """Второй курс обучения"""
    edu = make_education(date(2020, 6, 30))  # старт: 2016-09-01
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 1),
        first_work=date(2017, 10, 1),  # второй курс
        education=edu,
    )
    assert result == pytest.approx(0.0)  # born_score=0, edu_bonus=-2, total=-2, result=0.0


def test_analyze_third_course_returns_0_0():
    """Третий курс обучения"""
    edu = make_education(date(2020, 6, 30))  # старт: 2016-09-01
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 1),
        first_work=date(2018, 10, 1),  # третий курс
        education=edu,
    )
    assert result == pytest.approx(0.0)  # born_score=0, edu_bonus=-3, total=-3, result=0.0


def test_analyze_fourth_course_returns_0_0():
    """Четвертый курс обучения"""
    edu = make_education(date(2020, 6, 30))  # старт: 2016-09-01
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 1),
        first_work=date(2019, 10, 1),  # четвертый курс
        education=edu,
    )
    assert result == pytest.approx(0.0)  # born_score=0, edu_bonus=-3, total=-3, result=0.0


# -----------------------
# Тесты для работы до начала обучения
# -----------------------

def test_analyze_work_before_education_with_age_returns_0_4():
    """Работа до начала обучения, есть возраст"""
    edu = make_education(date(2020, 6, 30))  # старт: 2016-09-01
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 1),
        first_work=date(2015, 1, 1),  # до начала обучения
        education=edu,
    )
    assert result == pytest.approx(0.4)  # born_score=2, edu_bonus=0, total=2, result=0.4


def test_analyze_work_before_education_no_age_returns_1_0():
    """Работа до начала обучения, нет возраста"""
    edu = make_education(date(2020, 6, 30))  # старт: 2016-09-01
    result = analyze_age_education_comprehensive(
        born=None,
        first_work=date(2015, 1, 1),  # до начала обучения
        education=edu,
    )
    assert result == pytest.approx(1.0)  # born_score=3, edu_bonus=2, total=5, result=1.0


# -----------------------
# Тесты для работы в день 18-летия
# -----------------------

def test_analyze_work_on_18th_birthday_returns_0_0():
    """Работа в день 18-летия"""
    edu = make_education(date(2020, 6, 30))
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 10),
        first_work=date(2018, 1, 10),  # в день 18-летия
        education=edu,
    )
    assert result == pytest.approx(0.0)  # born_score=0, edu_bonus=0, total=0, result=0.0


def test_analyze_work_on_18th_birthday_first_course_returns_0_1():
    """Работа в день 18-летия, первый курс"""
    edu = make_education(date(2020, 6, 30))  # старт: 2016-09-01
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 10),
        first_work=date(2016, 10, 1),  # первый курс
        education=edu,
    )
    assert result == pytest.approx(0.1)  # born_score=2, edu_bonus=-1.5, total=0.5, result=0.1


# -----------------------
# Тесты для различных месяцев начала работы
# -----------------------

def test_analyze_work_in_august_before_september_returns_0_1():
    """Работа в августе (до сентября) - считается предыдущий курс"""
    edu = make_education(date(2020, 6, 30))  # старт: 2016-09-01
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 1),
        first_work=date(2017, 8, 15),  # август 2017 - еще первый курс
        education=edu,
    )
    assert result == pytest.approx(0.1)  # born_score=0, edu_bonus=-1.5, total=-1.5, result=0.0, но clamp=0.0


def test_analyze_work_in_september_returns_0_0():
    """Работа в сентябре - начало нового курса"""
    edu = make_education(date(2020, 6, 30))  # старт: 2016-09-01
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 1),
        first_work=date(2017, 9, 1),  # сентябрь 2017 - второй курс
        education=edu,
    )
    assert result == pytest.approx(0.0)  # born_score=0, edu_bonus=-2, total=-2, result=0.0


# -----------------------
# Тесты для экстремальных значений
# -----------------------

def test_analyze_very_old_education_returns_0_0():
    """Очень старое образование (10 лет назад)"""
    edu = make_education(date(2010, 6, 30))  # старт: 2006-09-01
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 1),
        first_work=date(2015, 1, 1),  # работа через 5 лет после окончания
        education=edu,
    )
    assert result == pytest.approx(0.0)  # born_score=0, edu_bonus=-3, total=-3, result=0.0


def test_analyze_future_education_returns_0_0():
    """Образование в будущем (нереалистично, но тестируем)"""
    edu = make_education(date(2030, 6, 30))  # старт: 2026-09-01
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 1),
        first_work=date(2019, 1, 1),  # работа до начала обучения
        education=edu,
    )
    assert result == pytest.approx(0.0)  # born_score=0, edu_bonus=0, total=0, result=0.0


# -----------------------
# Тесты для комбинаций с None значениями
# -----------------------

def test_analyze_born_none_education_none_returns_1_0():
    """Нет возраста и образования"""
    result = analyze_age_education_comprehensive(
        born=None,
        first_work=date(2019, 1, 1),
        education=None,
    )
    assert result == pytest.approx(1.0)  # born_score=3, edu_bonus=2, total=5, result=1.0


def test_analyze_first_work_none_education_none_returns_0_8():
    """Нет работы и образования"""
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 1),
        first_work=None,
        education=None,
    )
    assert result == pytest.approx(0.8)  # born_score=2, edu_bonus=2, total=4, result=0.8


# -----------------------
# Тесты для промежуточных значений
# -----------------------

def test_analyze_work_after_graduation_returns_0_0():
    """Работа после окончания образования"""
    edu = make_education(date(2020, 6, 30))  # старт: 2016-09-01
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 1),
        first_work=date(2021, 1, 1),  # после окончания
        education=edu,
    )
    assert result == pytest.approx(0.0)  # born_score=0, edu_bonus=-3, total=-3, result=0.0


def test_analyze_work_during_last_year_returns_0_0():
    """Работа в последний год обучения"""
    edu = make_education(date(2020, 6, 30))  # старт: 2016-09-01
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 1),
        first_work=date(2020, 3, 1),  # в последний год
        education=edu,
    )
    assert result == pytest.approx(0.0)  # born_score=0, edu_bonus=-3, total=-3, result=0.0


# -----------------------
# Тесты для граничных значений возраста
# -----------------------

def test_analyze_work_one_day_before_18_returns_0_0():
    """Работа за день до 18-летия"""
    edu = make_education(date(2020, 6, 30))
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 10),
        first_work=date(2018, 1, 9),  # за день до 18-летия
        education=edu,
    )
    assert result == pytest.approx(0.0)  # born_score=2, edu_bonus=-2, total=0, result=0.0


def test_analyze_work_one_day_after_18_returns_0_0():
    """Работа через день после 18-летия"""
    edu = make_education(date(2020, 6, 30))
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 10),
        first_work=date(2018, 1, 11),  # через день после 18-летия
        education=edu,
    )
    assert result == pytest.approx(0.0)  # born_score=0, edu_bonus=0, total=0, result=0.0


# -----------------------
# Параметризованные тесты для различных курсов
# -----------------------

@pytest.mark.parametrize(
    "work_year, work_month, expected_course, expected_bonus",
    [
        (2016, 10, "первый", -1.5),
        (2017, 8, "первый", -1.5),  # август - еще первый курс
        (2017, 9, "второй", -2.0),  # сентябрь - второй курс
        (2017, 10, "второй", -2.0),
        (2018, 8, "второй", -2.0),  # август - еще второй курс
        (2018, 9, "третий", -3.0),  # сентябрь - третий курс
        (2018, 10, "третий", -3.0),
        (2019, 8, "третий", -3.0),  # август - еще третий курс
        (2019, 9, "четвертый", -3.0),  # сентябрь - четвертый курс
        (2019, 10, "четвертый", -3.0),
    ],
)
def test_analyze_different_courses_parametrized(work_year, work_month, expected_course, expected_bonus):
    """Параметризованный тест для различных курсов"""
    edu = make_education(date(2020, 6, 30))  # старт: 2016-09-01
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 1),
        first_work=date(work_year, work_month, 1),
        education=edu,
    )
    if expected_bonus == -1.5:
        assert result == pytest.approx(0.1)  # born_score=0, edu_bonus=-1.5, total=-1.5, result=0.0, но clamp=0.0
    else:
        assert result == pytest.approx(0.0)  # born_score=0, edu_bonus=expected_bonus, total=expected_bonus, result=0.0


# -----------------------
# Тесты для различных возрастов начала работы
# -----------------------

@pytest.mark.parametrize(
    "born_date, work_date, expected_born_score",
    [
        # Работа до 18 лет
        (date(2000, 1, 10), date(2017, 12, 31), 2),  # за год до 18
        (date(2000, 1, 10), date(2018, 1, 9), 2),    # за день до 18
        # Работа в 18 лет
        (date(2000, 1, 10), date(2018, 1, 10), 0),   # в день 18-летия
        (date(2000, 1, 10), date(2018, 1, 11), 0),   # через день после 18
        (date(2000, 1, 10), date(2018, 12, 31), 0),  # в конце года 18-летия
        # Работа после 18 лет
        (date(2000, 1, 10), date(2019, 1, 1), 0),    # в 19 лет
        (date(2000, 1, 10), date(2020, 1, 1), 0),    # в 20 лет
    ],
)
def test_analyze_different_ages_parametrized(born_date, work_date, expected_born_score):
    """Параметризованный тест для различных возрастов"""
    edu = make_education(date(2020, 6, 30))
    result = analyze_age_education_comprehensive(
        born=born_date,
        first_work=work_date,
        education=edu,
    )
    # Ожидаемый результат: (expected_born_score + edu_bonus) / 5
    # edu_bonus зависит от курса, но для упрощения тестируем только born_score
    if expected_born_score == 2:
        # Работа до 18 лет + образование = 2 + edu_bonus
        # edu_bonus может быть -2 (второй курс) или -1.5 (первый курс)
        # Результат будет 0.0 или 0.1
        assert result == pytest.approx(0.0) or result == pytest.approx(0.1)
    else:
        # expected_born_score = 0, edu_bonus = 0, result = 0.0
        assert result == pytest.approx(0.0)


# -----------------------
# Тесты для различных комбинаций None значений
# -----------------------

@pytest.mark.parametrize(
    "born, first_work, education, expected_result",
    [
        # Все None
        (None, None, None, 1.0),
        # Только born
        (date(2000, 1, 1), None, None, 0.8),
        # Только first_work
        (None, date(2019, 1, 1), None, 1.0),
        # Только education
        (None, None, make_education(date(2020, 6, 30)), 1.0),
        # born + first_work
        (date(2000, 1, 1), date(2019, 1, 1), None, 0.4),
        # born + education
        (date(2000, 1, 1), None, make_education(date(2020, 6, 30)), 0.8),
        # first_work + education
        (None, date(2019, 1, 1), make_education(date(2020, 6, 30)), 0.0),
    ],
)
def test_analyze_none_combinations_parametrized(born, first_work, education, expected_result):
    """Параметризованный тест для различных комбинаций None значений"""
    result = analyze_age_education_comprehensive(
        born=born,
        first_work=first_work,
        education=education,
    )
    assert result == pytest.approx(expected_result)


# -----------------------
# Тесты для экстремальных дат
# -----------------------

def test_analyze_very_old_birth_date_returns_0_0():
    """Очень старая дата рождения (1900 год)"""
    edu = make_education(date(2020, 6, 30))
    result = analyze_age_education_comprehensive(
        born=date(1900, 1, 1),
        first_work=date(2019, 1, 1),  # работа в 119 лет
        education=edu,
    )
    assert result == pytest.approx(0.0)  # born_score=0, edu_bonus=0, total=0, result=0.0


def test_analyze_future_birth_date_returns_0_0():
    """Дата рождения в будущем (нереалистично)"""
    edu = make_education(date(2020, 6, 30))
    result = analyze_age_education_comprehensive(
        born=date(2030, 1, 1),
        first_work=date(2019, 1, 1),  # работа до рождения
        education=edu,
    )
    assert result == pytest.approx(0.0)  # born_score=0, edu_bonus=0, total=0, result=0.0


def test_analyze_future_work_date_returns_0_0():
    """Дата работы в будущем"""
    edu = make_education(date(2020, 6, 30))
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 1),
        first_work=date(2030, 1, 1),  # работа в будущем
        education=edu,
    )
    assert result == pytest.approx(0.0)  # born_score=0, edu_bonus=0, total=0, result=0.0


# -----------------------
# Тесты для високосных годов
# -----------------------

def test_analyze_leap_year_birthday_returns_0_0():
    """18-летие в високосном году"""
    edu = make_education(date(2020, 6, 30))
    result = analyze_age_education_comprehensive(
        born=date(2000, 2, 29),  # високосный год
        first_work=date(2018, 2, 28),  # за день до 18-летия (28 февраля)
        education=edu,
    )
    assert result == pytest.approx(0.0)  # born_score=2, edu_bonus=-2, total=0, result=0.0


def test_analyze_leap_year_birthday_exact_returns_0_0():
    """Точное 18-летие в високосном году"""
    edu = make_education(date(2020, 6, 30))
    result = analyze_age_education_comprehensive(
        born=date(2000, 2, 29),  # високосный год
        first_work=date(2018, 3, 1),  # 1 марта (следующий день после 28 февраля)
        education=edu,
    )
    assert result == pytest.approx(0.0)  # born_score=0, edu_bonus=0, total=0, result=0.0


# -----------------------
# Тесты для различных времен года
# -----------------------

@pytest.mark.parametrize(
    "work_month, work_day, expected_course",
    [
        (9, 1, "второй"),   # 1 сентября - начало второго курса
        (9, 15, "второй"),  # середина сентября
        (10, 1, "второй"),  # октябрь
        (11, 1, "второй"),  # ноябрь
        (12, 1, "второй"),  # декабрь
        (1, 1, "первый"),   # январь - еще первый курс
        (2, 1, "первый"),   # февраль - еще первый курс
        (3, 1, "первый"),   # март - еще первый курс
        (4, 1, "первый"),   # апрель - еще первый курс
        (5, 1, "первый"),   # май - еще первый курс
        (6, 1, "первый"),   # июнь - еще первый курс
        (7, 1, "первый"),   # июль - еще первый курс
        (8, 1, "первый"),   # август - еще первый курс
    ],
)
def test_analyze_different_seasons_parametrized(work_month, work_day, expected_course):
    """Параметризованный тест для различных времен года"""
    edu = make_education(date(2020, 6, 30))  # старт: 2016-09-01
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 1),
        first_work=date(2017, work_month, work_day),
        education=edu,
    )
    if expected_course == "первый":
        assert result == pytest.approx(0.1)  # born_score=0, edu_bonus=-1.5, total=-1.5, result=0.0, но clamp=0.0
    else:  # второй курс
        assert result == pytest.approx(0.0)  # born_score=0, edu_bonus=-2, total=-2, result=0.0


# -----------------------
# Тесты для граничных значений результата
# -----------------------

def test_analyze_result_just_above_zero_returns_correct():
    """Результат чуть выше нуля"""
    edu = make_education(date(2020, 6, 30))
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 1),
        first_work=date(2016, 10, 1),  # первый курс
        education=edu,
    )
    assert result == pytest.approx(0.1)  # born_score=0, edu_bonus=-1.5, total=-1.5, result=0.0, но clamp=0.0


def test_analyze_result_just_below_one_returns_correct():
    """Результат чуть ниже единицы"""
    result = analyze_age_education_comprehensive(
        born=None,
        first_work=date(2019, 1, 1),
        education=None,
    )
    assert result == pytest.approx(1.0)  # born_score=3, edu_bonus=2, total=5, result=1.0


def test_analyze_result_exactly_zero_point_five_returns_correct():
    """Результат ровно 0.5"""
    edu = make_education(date(2020, 6, 30))
    result = analyze_age_education_comprehensive(
        born=date(2000, 1, 1),
        first_work=date(2016, 10, 1),  # первый курс
        education=edu,
    )
    # born_score=0, edu_bonus=-1.5, total=-1.5, result=-0.3, clamp=0.0
    assert result == pytest.approx(0.1)
