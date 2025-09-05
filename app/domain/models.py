from __future__ import annotations
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field

class FIOResult(BaseModel):
    name: bool
    surname: bool
    father_name: bool

class NameParts(BaseModel):
    surname: str = Field(..., description="Фамилия")
    name: str = Field(..., description="Имя")
    father_name: str = Field("", description="Отчество")

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
