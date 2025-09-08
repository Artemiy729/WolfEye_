from app.domain.models import NameParts
from app.application.services.fio import check_fio

def main():
    
    
    print(check_fio(NameParts(surname="Джун", name="Дмитрий", father_name="Михайлович")))

if __name__ == "__main__":
    main()