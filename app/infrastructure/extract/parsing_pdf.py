from __future__ import annotations
from app.domain.models import Rezume, NameParts, Education, EducationEntry

class ExtractData:
    def __init__(self):
        pass

    def extract(self, path: str) -> Rezume:
        # Мокаем извлечение данных из PDF — возвращаем демо-резюме
        fio = NameParts(surname="Иванов", name="Иван", father_name="Иванович")
        edu = Education(higher=True, items=[EducationEntry(university="МГУ", city="Москва")])
        return Rezume(
            fio=fio,
            residence_city="Москва",
            desired_position="Python-разработчик",
            education=edu,
            skills=["Python", "Pydantic", "SQL"],
            about="Проверочный мок."
        )
