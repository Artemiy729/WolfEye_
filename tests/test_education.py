import pytest
from datetime import date, timedelta
from app.application.services.education import (
    analyze_education,
    _is_education_basic_complete,
    _is_education_finished
)
from app.domain.models import Education, EducationEntry


class TestAnalyzeEducation:
    """Тесты для функции analyze_education"""
    
    def test_no_education_data(self):
        """Тест: нет данных об образовании - возвращает 1.0"""
        education = Education()
        result = analyze_education(education, "Москва")
        assert result == 1.0
    
    def test_empty_education_items(self):
        """Тест: пустой список образований - возвращает 1.0"""
        education = Education(items=[])
        result = analyze_education(education, "Москва")
        assert result == 1.0
    
    def test_none_education(self):
        """Тест: None вместо образования - возвращает 1.0"""
        result = analyze_education(None, "Москва")
        assert result == 1.0
    
    def test_incomplete_basic_data(self):
        """Тест: неполные базовые данные - возвращает 1.0"""
        # Нет университета
        edu_entry = EducationEntry(
            university=None,
            city="Москва",
            faculty="Информатика"
        )
        education = Education(items=[edu_entry])
        result = analyze_education(education, "Москва")
        assert result == 1.0
        
        # Нет города
        edu_entry = EducationEntry(
            university="МГУ",
            city=None,
            faculty="Информатика"
        )
        education = Education(items=[edu_entry])
        result = analyze_education(education, "Москва")
        assert result == 1.0
        
        # Нет факультета
        edu_entry = EducationEntry(
            university="МГУ",
            city="Москва",
            faculty=None
        )
        education = Education(items=[edu_entry])
        result = analyze_education(education, "Москва")
        assert result == 1.0
        
        # Пустые строки
        edu_entry = EducationEntry(
            university="",
            city="Москва",
            faculty="Информатика"
        )
        education = Education(items=[edu_entry])
        result = analyze_education(education, "Москва")
        assert result == 1.0
    
    def test_education_finished(self):
        """Тест: образование окончено - возвращает 0.0"""
        edu_entry = EducationEntry(
            university="МГУ",
            city="Москва",
            faculty="Информатика",
            end_date=date(2020, 6, 1)
        )
        education = Education(items=[edu_entry])
        result = analyze_education(education, "Москва")
        assert result == 0.0
    
    def test_education_not_finished_same_city(self):
        """Тест: образование не окончено, город совпадает - возвращает 0.0"""
        future_date = date.today() + timedelta(days=365)
        edu_entry = EducationEntry(
            university="МГУ",
            city="Москва",
            faculty="Информатика",
            end_date=future_date
        )
        education = Education(items=[edu_entry])
        result = analyze_education(education, "Москва")
        assert result == 0.0
    
    def test_education_not_finished_different_city(self):
        """Тест: образование не окончено, город не совпадает - возвращает 0.75"""
        future_date = date.today() + timedelta(days=365)
        edu_entry = EducationEntry(
            university="СПбГУ",
            city="Санкт-Петербург",
            faculty="Информатика",
            end_date=future_date
        )
        education = Education(items=[edu_entry])
        result = analyze_education(education, "Москва")
        assert result == 0.75
    
    def test_education_no_end_date_same_city(self):
        """Тест: нет даты окончания, город совпадает - возвращает 0.0"""
        edu_entry = EducationEntry(
            university="МГУ",
            city="Москва",
            faculty="Информатика",
            end_date=None
        )
        education = Education(items=[edu_entry])
        result = analyze_education(education, "Москва")
        assert result == 0.0
    
    def test_education_no_end_date_different_city(self):
        """Тест: нет даты окончания, город не совпадает - возвращает 0.75"""
        edu_entry = EducationEntry(
            university="СПбГУ",
            city="Санкт-Петербург",
            faculty="Информатика",
            end_date=None
        )
        education = Education(items=[edu_entry])
        result = analyze_education(education, "Москва")
        assert result == 0.75
    
    def test_city_comparison_variations(self):
        """Тест: различные варианты сравнения городов"""
        edu_entry = EducationEntry(
            university="МГУ",
            city="Москва",
            faculty="Информатика",
            end_date=None
        )
        education = Education(items=[edu_entry])
        
        # Разные варианты написания Москвы
        result1 = analyze_education(education, "Москва")
        result2 = analyze_education(education, "москва")
        result3 = analyze_education(education, "МОСКВА")
        result4 = analyze_education(education, "г. Москва")
        
        # Первые три должны возвращать 0.0 (город совпадает)
        # Четвертый - 0.75 (город не совпадает из-за префикса "г.")
        assert result1 == 0.0
        assert result2 == 0.0
        assert result3 == 0.0
        assert result4 == 0.75


class TestIsEducationBasicComplete:
    """Тесты для функции _is_education_basic_complete"""
    
    def test_complete_data(self):
        """Тест: все базовые данные заполнены"""
        edu_entry = EducationEntry(
            university="МГУ",
            city="Москва",
            faculty="Информатика"
        )
        assert _is_education_basic_complete(edu_entry) is True
    
    def test_missing_university(self):
        """Тест: отсутствует университет"""
        edu_entry = EducationEntry(
            university=None,
            city="Москва",
            faculty="Информатика"
        )
        assert _is_education_basic_complete(edu_entry) is False
    
    def test_empty_university(self):
        """Тест: пустая строка университета"""
        edu_entry = EducationEntry(
            university="",
            city="Москва",
            faculty="Информатика"
        )
        assert _is_education_basic_complete(edu_entry) is False
    
    def test_whitespace_university(self):
        """Тест: университет из пробелов"""
        edu_entry = EducationEntry(
            university="   ",
            city="Москва",
            faculty="Информатика"
        )
        assert _is_education_basic_complete(edu_entry) is False
    
    def test_missing_city(self):
        """Тест: отсутствует город"""
        edu_entry = EducationEntry(
            university="МГУ",
            city=None,
            faculty="Информатика"
        )
        assert _is_education_basic_complete(edu_entry) is False
    
    def test_empty_city(self):
        """Тест: пустая строка города"""
        edu_entry = EducationEntry(
            university="МГУ",
            city="",
            faculty="Информатика"
        )
        assert _is_education_basic_complete(edu_entry) is False
    
    def test_missing_faculty(self):
        """Тест: отсутствует факультет"""
        edu_entry = EducationEntry(
            university="МГУ",
            city="Москва",
            faculty=None
        )
        assert _is_education_basic_complete(edu_entry) is False
    
    def test_empty_faculty(self):
        """Тест: пустая строка факультета"""
        edu_entry = EducationEntry(
            university="МГУ",
            city="Москва",
            faculty=""
        )
        assert _is_education_basic_complete(edu_entry) is False
    
    def test_multiple_missing_fields(self):
        """Тест: отсутствует несколько полей"""
        edu_entry = EducationEntry(
            university=None,
            city=None,
            faculty="Информатика"
        )
        assert _is_education_basic_complete(edu_entry) is False


class TestIsEducationFinished:
    """Тесты для функции _is_education_finished"""
    
    def test_finished_education_past_date(self):
        """Тест: образование окончено (дата в прошлом)"""
        past_date = date.today() - timedelta(days=365)
        edu_entry = EducationEntry(
            university="МГУ",
            city="Москва",
            faculty="Информатика",
            end_date=past_date
        )
        assert _is_education_finished(edu_entry) is True
    
    def test_unfinished_education_future_date(self):
        """Тест: образование не окончено (дата в будущем)"""
        future_date = date.today() + timedelta(days=365)
        edu_entry = EducationEntry(
            university="МГУ",
            city="Москва",
            faculty="Информатика",
            end_date=future_date
        )
        assert _is_education_finished(edu_entry) is False
    
    def test_no_end_date(self):
        """Тест: нет даты окончания"""
        edu_entry = EducationEntry(
            university="МГУ",
            city="Москва",
            faculty="Информатика",
            end_date=None
        )
        assert _is_education_finished(edu_entry) is False
    
    def test_today_end_date(self):
        """Тест: дата окончания сегодня"""
        today = date.today()
        edu_entry = EducationEntry(
            university="МГУ",
            city="Москва",
            faculty="Информатика",
            end_date=today
        )
        # Дата сегодня считается не оконченной (строго меньше сегодняшней даты)
        assert _is_education_finished(edu_entry) is False
    
    def test_yesterday_end_date(self):
        """Тест: дата окончания вчера"""
        yesterday = date.today() - timedelta(days=1)
        edu_entry = EducationEntry(
            university="МГУ",
            city="Москва",
            faculty="Информатика",
            end_date=yesterday
        )
        assert _is_education_finished(edu_entry) is True


class TestEdgeCases:
    """Тесты для граничных случаев"""
    
    def test_multiple_education_entries(self):
        """Тест: несколько записей об образовании (берется первая)"""
        edu_entry1 = EducationEntry(
            university="МГУ",
            city="Москва",
            faculty="Информатика",
            end_date=date(2020, 6, 1)
        )
        edu_entry2 = EducationEntry(
            university="СПбГУ",
            city="Санкт-Петербург",
            faculty="Математика",
            end_date=None
        )
        education = Education(items=[edu_entry1, edu_entry2])
        result = analyze_education(education, "Москва")
        # Должна использоваться первая запись (оконченное образование)
        assert result == 0.0
    
    def test_very_old_education(self):
        """Тест: очень старое образование"""
        old_date = date(1990, 6, 1)
        edu_entry = EducationEntry(
            university="МГУ",
            city="Москва",
            faculty="Информатика",
            end_date=old_date
        )
        education = Education(items=[edu_entry])
        result = analyze_education(education, "Москва")
        assert result == 0.0
    
    def test_very_future_education(self):
        """Тест: очень далекое будущее образование"""
        future_date = date.today() + timedelta(days=3650)  # 10 лет в будущем
        edu_entry = EducationEntry(
            university="МГУ",
            city="Москва",
            faculty="Информатика",
            end_date=future_date
        )
        education = Education(items=[edu_entry])
        result = analyze_education(education, "Москва")
        assert result == 0.0  # Город совпадает
    
    def test_very_future_education_different_city(self):
        """Тест: очень далекое будущее образование в другом городе"""
        future_date = date.today() + timedelta(days=3650)  # 10 лет в будущем
        edu_entry = EducationEntry(
            university="СПбГУ",
            city="Санкт-Петербург",
            faculty="Информатика",
            end_date=future_date
        )
        education = Education(items=[edu_entry])
        result = analyze_education(education, "Москва")
        assert result == 0.75  # Город не совпадает
