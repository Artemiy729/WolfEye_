from app.domain.models import NameParts
from app.application.services.fio import analysis_fio
from app.application.services.born import when_start_working
from datetime import date
import time

def main():
    
  
    # start = time.perf_counter()
    # res1 = analysis_fio(NameParts(surname="Смирнов", name="Александр", father_name="Вячеславович"))
    # end = time.perf_counter()
    # print(res1, "вероятность:" + str(res1.suspicion_score()), f"(заняло {end - start:.3f} сек)")


    
    result1 = when_start_working(born=None, first_work=date(2020, 1, 1), end_university=None)
    print(result1)
    
   
    
    # core = CoreML()
    # score = core.get_score(rezume, llm)

    # print("Резюме:", rezume.model_dump())
    # print("Скор:", score)

if __name__ == "__main__":
    main()
