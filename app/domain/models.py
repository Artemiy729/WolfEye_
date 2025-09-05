from __future__ import annotations
from datetime import date
from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class FIOResult(BaseModel):
    name: bool
    surname: bool
    father_name: bool
    @staticmethod
    def _parse_flags(s: str) -> Dict[str, bool]:
        s = s.strip()
        if len(s) != 3 or any(ch not in "01" for ch in s):
            raise ValueError(
                "Ожидается строка из 3 символов '0'/'1', например: '101'."
            )
        return {
            "name": s[0] == "1",
            "surname": s[1] == "1",
            "father_name": s[2] == "1",
        }

    def __init__(self, *args, **kwargs):
        # Разрешаем вызов FIOResult("101")
        if args and isinstance(args[0], str) and not kwargs:
            kwargs = self._parse_flags(args[0])
        elif args:
            # Запрещаем позиционные аргументы помимо единственной строки
            raise TypeError(
                "Используйте FIOResult('101') или именованные аргументы: "
                "FIOResult(name=True, surname=False, father_name=True)."
            )
        super().__init__(**kwargs)


class NameParts(BaseModel):
    surname: str = Field(..., description="Фамилия")
    name: str = Field(..., description="Имя")
    father_name: str = Field("", description="Отчество")

    def __str__(self) -> str:
        return " ".join(part for part in [self.surname, self.name, self.father_name] if part)


class PlaceWork(BaseModel):
    company: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    company_info: Optional[str] = None
    position: Optional[str] = None
    legend: Optional[str] = None


class EducationEntry(BaseModel):
    university: Optional[str] = None
    city: Optional[str] = None
    faculty: Optional[str] = None
    end_date: Optional[date] = None


class Education(BaseModel):
    higher: Optional[bool] = None
    items: List[EducationEntry] = []


class Rezume(BaseModel):
    fio: NameParts
    born_date: Optional[date] = None
    phone: Optional[str] = None
    residence_city: Optional[str] = None
    desired_position: Optional[str] = None
    experience_years: Optional[int] = None
    places: List[PlaceWork] = []
    education: Education = Education()
    skills: List[str] = []
    about: Optional[str] = None
