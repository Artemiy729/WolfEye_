import json
from app.application.services.age_education_analysis import analyze_age_education_comprehensive
from app.application.services.company import analyze_company
from app.application.services.education import analyze_education
from app.domain.models import Education, NameParts, PlaceWork, Rezume
from app.application.services.fio import check_fio
from app.application.core import CoreML

def main():
    for i in range(1, 7):
        with open(f"resources/sample_resumes/{i}.json", "r") as f:
            data = json.load(f)
            fio = NameParts(surname=data["fio"]["surname"], name=data["fio"]["name"], father_name=data["fio"]["father_name"])
            born_date = data["born_date"]
            phone = data["phone"]
            residence_city = data["residence_city"]
            desired_position = data["desired_position"]
            experience_years = data["experience_years"]
            places = [PlaceWork(company=place["company"], start_date=place["start_date"], end_date=place["end_date"], company_info=place["company_info"], position=place["position"], legend=place["legend"]) for place in data["places"]]
            first_work = data["places"][0]["start_date"]
            education = Education(higher=data["education"]["higher"], items=data["education"]["items"])
            skills = data["skills"]
            about = data["about"]
        
            resume = Rezume(fio=fio, born_date=born_date, phone=phone, residence_city=residence_city, desired_position=desired_position, experience_years=experience_years, places=places, first_work=first_work, education=education, skills=skills, about=about)
            
            ml = CoreML()
            final_score = ml.get_score(resume)
            print(i, final_score)
    ### Прогон чистой резюме      
    with open(f"resources/sample_resumes/clean.json", "r") as f:
            data = json.load(f)
            fio = NameParts(surname=data["fio"]["surname"], name=data["fio"]["name"], father_name=data["fio"]["father_name"])
            born_date = data["born_date"]
            phone = data["phone"]
            residence_city = data["residence_city"]
            desired_position = data["desired_position"]
            experience_years = data["experience_years"]
            places = [PlaceWork(company=place["company"], start_date=place["start_date"], end_date=place["end_date"], company_info=place["company_info"], position=place["position"], legend=place["legend"]) for place in data["places"]]
            first_work = data["places"][0]["start_date"]
            education = Education(higher=data["education"]["higher"], items=data["education"]["items"])
            skills = data["skills"]
            about = data["about"]
        
            resume = Rezume(fio=fio, born_date=born_date, phone=phone, residence_city=residence_city, desired_position=desired_position, experience_years=experience_years, places=places, first_work=first_work, education=education, skills=skills, about=about)
            
            ml = CoreML()
            final_score = ml.get_score(resume)
            print("clean_resume", final_score)
            
            
    
    
<<<<<<< Updated upstream
    print(check_fio(NameParts(surname="Джун", name="Дмитрий", father_name="Михайлович")))
=======

>>>>>>> Stashed changes

if __name__ == "__main__":
    main()