from app.domain.models import NameParts, Education, EducationEntry
from app.application.services.fio import analysis_fio
from app.application.services.born import when_start_working
from app.application.services.study import analyze_education
from datetime import date
import time

def main():
    
  
    start = time.perf_counter()
    res1 = analysis_fio(NameParts(surname="Смирнов", name="Александр", father_name="Вячеславович"))
    end = time.perf_counter()
    print(res1, "вероятность:" + str(res1.suspicion_score()), f"(заняло {end - start:.3f} сек)")



    born_score = when_start_working(
        born=date(2006, 5, 15), 
        first_work=date(2014, 6, 1),
        end_university=None
    )
    print(born_score)

 
    education = Education(items=[
        EducationEntry(
            university="МГУ", 
            city="Москва", 
            faculty="Информатика и вычислительная техника", 
            end_date=date(2026, 6, 30)
        )
    ])
    education_score = analyze_education(education, "Санкт-Петербург")
    print(education_score)
    
    
    ###
    
    # core = CoreML()
    # score = core.get_score(rezume, llm)

    # print("Резюме:", rezume.model_dump())
    # print("Скор:", score)

if __name__ == "__main__":
    main()
