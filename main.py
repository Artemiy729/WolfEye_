from app.domain.models import NameParts
from app.application.services.fio import analysis_fio
import time

def main():
    
    start = time.perf_counter()
    res1 = analysis_fio(NameParts(surname="Смирнов", name="Александр", father_name="Вячеславович"))
    end = time.perf_counter()
    print(res1, "вероятность:" + str(res1.suspicion_score()), f"(заняло {end - start:.3f} сек)")

    start = time.perf_counter()
    res2 = analysis_fio(NameParts(surname="Сидр", name="Иван", father_name="Ивaнович"))
    end = time.perf_counter()
    print(res2, "вероятность:" + str(res2.suspicion_score()), f"(заняло {end - start:.3f} сек)")

    start = time.perf_counter()
    res3 = analysis_fio(NameParts(surname="Ф)торович", name="Иван", father_name="Математикович"))
    end = time.perf_counter()
    print(res3, "вероятность:" + str(res3.suspicion_score()), f"(заняло {end - start:.3f} сек)")
    
    
    # core = CoreML()
    # score = core.get_score(rezume, llm)

    # print("Резюме:", rezume.model_dump())
    # print("Скор:", score)

if __name__ == "__main__":
    main()
