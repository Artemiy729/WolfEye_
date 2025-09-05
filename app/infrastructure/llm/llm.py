from __future__ import annotations
from typing import Dict
from app.config import CONFIG
from .prompts.system_prompts import ANALIZ_LEGEND
from .prompts.user_prompts import PARSING_PDF
from app.domain.models import FIOResult, NameParts

class LLM:
    def __init__(self):
        # Инициализация с токенами (мок конфиг)
        self.Model: Dict = CONFIG

    def checking_FIO(self, data: NameParts) -> FIOResult:
        # Проверяет ФИО человека на опечатки (мок — все True)
        return FIOResult(name=True, surname=True, father_name=True)

    def analysis_of_legend(self, text: str, patterns: dict[int, str]) -> int:
        # Анализ легенды резюме на предмет накрутки (мок — 1)
        return 1
