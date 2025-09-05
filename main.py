from app.domain.models import NameParts
from app.application.services.fio import analysis_fio

import time

def main():

    start = time.perf_counter()
    res1 = analysis_fio(NameParts(surname="Иванова", name="Ивaн", father_name="Ивaн0вич"))
    end = time.perf_counter()
    print(res1, f"(заняло {end - start:.3f} сек)")

    start = time.perf_counter()
    res2 = analysis_fio(NameParts(surname="Пидоров", name="Иван", father_name="Ивaнович"))
    end = time.perf_counter()
    print(res2, f"(заняло {end - start:.3f} сек)")

    start = time.perf_counter()
    res2 = analysis_fio(NameParts(surname="Сидоров", name="Иван", father_name="Ивaнович"))
    end = time.perf_counter()
    print(res2, f"(заняло {end - start:.3f} сек)")
    # core = CoreML()
    # score = core.get_score(rezume, llm)

    # print("Резюме:", rezume.model_dump())
    # print("Скор:", score)

if __name__ == "__main__":
    main()
