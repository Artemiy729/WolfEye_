from app.application.services.born import when_start_working
from app.application.services.city import compare_cities
from app.application.services.fio import analysis_fio
from app.application.services.legend import analysis_legend

from app.domain.models import Rezume, PlaceWork

class CoreML:
    def __init__(self):
        pass

    def get_score(self, rezume: Rezume) -> int:
        # Мок: просто возвращаем 1 как интегральный скор
        return 1
