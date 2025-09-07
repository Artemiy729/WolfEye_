from app.application.services.age_education_analysis import analyze_age_education_comprehensive
from app.application.services.company import analyze_company
from app.application.services.education import analyze_education
from app.application.services.fio import check_fio

from app.domain.models import Rezume

### Пока неизвестна функция финального просчета, поэтому решил пока оставить как есть
class CoreML:
    def __init__(self):
        pass

    def get_score(self, rezume: Rezume) -> int:
        fio_score = check_fio(rezume.fio)
        age_education_score = analyze_age_education_comprehensive(rezume.born_date, rezume.first_work, rezume.education)
        education_score = analyze_education(rezume.education, rezume.residence_city)
        company_score = analyze_company(rezume.places)
        
        final_score = fio_score * 60 + age_education_score * 40 + education_score * 20 + company_score * 10

        if final_score > 100:
            final_score = 100

        return final_score 
