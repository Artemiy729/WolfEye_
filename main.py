from app.domain.models import NameParts, Education, EducationEntry
from app.application.services.fio import analysis_fio, calculate_suspicion_score
from app.application.services.age_education_analysis import when_start_working, analyze_age_education_comprehensive
from app.application.services.higher import analyze_education
from app.application.services.city import compare_cities
from datetime import date
import time

def main():
    
    
    # 1. Анализ ФИО
    start = time.perf_counter()
    fio_result = analysis_fio(NameParts(surname="Смиpнов", name="Александр", father_name="Вячеславович"))
    end = time.perf_counter()
    suspicion_score = calculate_suspicion_score(fio_result)
    print(f"ФИО: {fio_result}")
    print(f"Коэффициент подозрительности: {suspicion_score:.3f}")
    print(f"Время выполнения: {end - start:.3f} сек")
    
    # 2. Анализ возраста и работы

    start = time.perf_counter()
    age_score = when_start_working(
        born=date(1995, 1, 1), 
        first_work=date(2020, 1, 1),  # 25 лет
        end_university=None
    )
    end = time.perf_counter()
    print(f"Дата рождения: 1995-01-01")
    print(f"Дата первой работы: 2020-01-01 (25 лет)")
    print(f"Штрафные баллы: {age_score}")
    print(f"Время выполнения: {end - start:.3f} сек")
    
    ##
    start = time.perf_counter()
    age_score = when_start_working(
        born=date(1995, 1, 1), 
        first_work=date(1996, 1, 1),  # 1 год
        end_university=None
    )
    end = time.perf_counter()
    print(f"Дата рождения: 1995-01-01")
    print(f"Дата первой работы: 1996-01-01 (1 год)")
    print(f"Штрафные баллы: {age_score}")
    print(f"Время выполнения: {end - start:.3f} сек")
    
    # 3. Анализ образования
    education = Education(items=[
        EducationEntry(
            university="МГУ", 
            city="Москва", 
            faculty="Информатика и вычислительная техника", 
            end_date=date(2020, 6, 30)
        )
    ])
    start = time.perf_counter()
    education_score = analyze_education(education, "Москва")
    end = time.perf_counter()
    print(f"Университет: МГУ, Москва")
    print(f"Факультет: Информатика и вычислительная техника")
    print(f"Дата окончания: 2020-06-30")
    print(f"Город проживания: Москва")
    print(f"Коэффициент подозрительности: {education_score:.3f}")
    print(f"Время выполнения: {end - start:.3f} сек")
    
    
    education = Education(items=[
        EducationEntry(
            university="МГУ", 
            city="Москва", 
            faculty="Информатика и вычислительная техника", 
            end_date=date(2026, 6, 30)
        )
    ])
    start = time.perf_counter()
    education_score = analyze_education(education, "Санкт-Петербург")
    end = time.perf_counter()
    print(f"Университет: МГУ, Москва")
    print(f"Факультет: Информатика и вычислительная техника")
    print(f"Дата окончания: 2026-06-30")
    print(f"Город проживания: Санкт-Петербург")
    print(f"Коэффициент подозрительности: {education_score:.3f}")
    print(f"Время выполнения: {end - start:.3f} сек")
    
    
    #  Дата рождения + образование - НОРМАЛЬНЫЙ СЛУЧАЙ
    start = time.perf_counter()
    comprehensive_score = analyze_age_education_comprehensive(
        born=date(1995, 1, 1),
        first_work=date(2021, 1, 1),  # После окончания
        education=education,
        residence_city="Москва"
    )
    end = time.perf_counter()
    print(f"Дата рождения: 1995-01-01")
    print(f"Дата первой работы: 2021-01-01")
    print(f"Образование: МГУ, Москва (завершено)")
    print(f"Город проживания: Москва")
    print(f"Итоговый коэффициент подозрительности: {comprehensive_score:.3f}")
    print(f"Время выполнения: {end - start:.3f} сек")
    
    #  Нет даты рождения + незавершенное образование в другом городе

    suspicious_education = Education(items=[
        EducationEntry(
            university="СПбГУ", 
            city="Санкт-Петербург", 
            faculty="Математика", 
            end_date=date(2026, 6, 30)  # Будущая дата - не завершено
        )
    ])
    start = time.perf_counter()
    suspicious_score = analyze_age_education_comprehensive(
        born=None,  # Нет даты рождения
        first_work=date(2015, 1, 1),  # Работа в 15 лет (если бы была дата рождения)
        education=suspicious_education,
        residence_city="Москва"  # Другой город
    )
    end = time.perf_counter()
    print(f"Дата рождения: нет")
    print(f"Дата первой работы: 2015-01-01")
    print(f"Образование: СПбГУ, Санкт-Петербург (не завершено)")
    print(f"Город проживания: Москва")
    print(f"Итоговый коэффициент подозрительности: {suspicious_score:.3f}")
    print(f"Время выполнения: {end - start:.3f} сек")
    
    
    

if __name__ == "__main__":
    main()
