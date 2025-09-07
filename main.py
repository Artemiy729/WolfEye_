from app.application.services.company import analyze_company
from app.domain.models import NameParts, Education, EducationEntry, PlaceWork
from app.application.services.fio import analysis_fio, calculate_suspicion_score
from app.application.services.age_education_analysis import when_start_working, analyze_age_education_comprehensive
from app.application.services.higher import analyze_education
from app.application.services.city import compare_cities
from datetime import date
import time

def main():
    
    
    # 1. Анализ ФИО
    
    fio_result = analysis_fio(NameParts(surname="Смирнов", name="ываыва", father_name="Петрович"))
    
    suspicion_score = calculate_suspicion_score(fio_result)
    print(f"ФИО: {fio_result}")
    print(f"Коэффициент подозрительности: {suspicion_score:.3f}")
   
    

    
    
    # 2. Анализ Вуза
    education = Education(items=[
        EducationEntry(
            university="МГУ", 
            city="Москва", 
            faculty="Информатика и вычислительная техника", 
            end_date=date(2020, 6, 30)
        )
    ])
    
    education_score = analyze_education(education, "Москва")
    
    print(f"Университет: МГУ, Москва")
    print(f"Факультет: Информатика и вычислительная техника")
    print(f"Дата окончания: 2020-06-30")
    print(f"Город проживания: Москва")
    print(f"Коэффициент подозрительности: {education_score:.3f}")
    
    
    
    education = Education(items=[
        EducationEntry(
            university="МГУ", 
            city="Москва", 
            faculty="Информатика и вычислительная техника", 
            end_date=date(2026, 6, 30)
        )
    ])
    
    education_score = analyze_education(education, "Санкт-Петербург")
    
    print(f"Университет: МГУ, Москва")
    print(f"Факультет: Информатика и вычислительная техника")
    print(f"Дата окончания: 2026-06-30")
    print(f"Город проживания: Санкт-Петербург")
    print(f"Коэффициент подозрительности: {education_score:.3f}")
    
    
    
    #  3. Анализ Дата рождения + образование - НОРМАЛЬНЫЙ СЛУЧАЙ
    
    comprehensive_score = analyze_age_education_comprehensive(
        born=date(1995, 1, 1),
        first_work=date(2021, 1, 1),  # После окончания
        education=education,
        residence_city="Москва"
    )
    
    print(f"Дата рождения: 1995-01-01")
    print(f"Дата первой работы: 2021-01-01")
    print(f"Образование: МГУ, Москва (завершено)")
    print(f"Город проживания: Москва")
    print(f"Итоговый коэффициент подозрительности: {comprehensive_score:.3f}")
    
    
    #  Нет даты рождения + незавершенное образование в другом городе

    suspicious_education = Education(items=[
        EducationEntry(
            university="СПбГУ", 
            city="Санкт-Петербург", 
            faculty="Математика", 
            end_date=date(2026, 6, 30)  # Будущая дата - не завершено
        )
    ])
    
    suspicious_score = analyze_age_education_comprehensive(
        born=None,  # Нет даты рождения
        first_work=date(2015, 1, 1),  
        education=suspicious_education,
        residence_city="Москва"  # Другой город
    )
    
    print(f"Дата рождения: нет")
    print(f"Дата первой работы: 2015-01-01")
    print(f"Образование: СПбГУ, Санкт-Петербург (не завершено)")
    print(f"Город проживания: Москва")
    print(f"Итоговый коэффициент подозрительности: {suspicious_score:.3f}")
    
    ### 4. Анализ компании
    ### Нет компании
    suspicious_company = PlaceWork(company=None)
    suspicious_company_score = analyze_company(suspicious_company)
    
    print(f"Компания: нет")
    print(f"Коэффициент подозрительности: {suspicious_company_score:.3f}")
    
    ### Есть компания
    normal_company = PlaceWork(company="ООО 'Рога и копыта'")
    normal_company_score = analyze_company(normal_company)
    
    print(f"Компания: ООО 'Рога и копыта'")
    print(f"Коэффициент подозрительности: {normal_company_score:.3f}")
    

if __name__ == "__main__":
    main()
