from __future__ import annotations
from datetime import date
from typing import Optional, List, Dict, ClassVar
from pydantic import BaseModel, Field, field_validator


class FIOResult(BaseModel):
    name: int
    surname: int
    father_name: int
    
    ALLOWED: ClassVar[set[int]] = {0, 1, 2, 4}
    
    @staticmethod
    def _parse_flags(s: str) -> Dict[str, int]:
        s = s.strip()
        if len(s) != 3 or any(ch not in "0124" for ch in s):
            raise ValueError(
                "Ожидается строка из трёх символов из {0,1,2,4}, например: '024'."
            )
        return {
            "surname": int(s[0]),
            "name": int(s[1]),
            "father_name": int(s[2]),
        }

    def __init__(self, *args, **kwargs):
        # Разрешаем вызов FIOResult("024")
        if args and isinstance(args[0], str) and not kwargs:
            kwargs = self._parse_flags(args[0])
        elif args:
            # Запрещаем позиционные аргументы помимо единственной строки
            raise TypeError(
                "Используйте FIOResult('024') или именованные аргументы: "
                "FIOResult(name=0, surname=2, father_name=4)."
            )
        super().__init__(**kwargs)
        
    @field_validator("surname", "name", "father_name", mode="before")
    @classmethod
    def _force_and_check(cls, v):
        # принимаем и '0'/'1'/'2'/'4', и int
        if isinstance(v, str):
            if v not in {"0", "1", "2", "4"}:
                raise ValueError(f"Значение должно быть одним из {cls.ALLOWED}, получено {v!r}")
            v = int(v)
        if not isinstance(v, int):
            raise TypeError("Ожидается целое число из {0,1,2,4}")
        if v not in cls.ALLOWED:
            raise ValueError(f"Значение должно быть одним из {cls.ALLOWED}, получено {v}")
        return v


    def suspicion_score(self) -> float:
        s = self.surname + self.name + self.father_name
        return min(1.0, s / 5.0)

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
