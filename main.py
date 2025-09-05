from app.infrastructure.llm.llm import LLM
from app.application.services.core import CoreML
from app.infrastructure.extract.parsing_pdf import ExtractData

def main():
    extractor = ExtractData()
    rezume = extractor.extract("resume.pdf")
    llm = LLM()
    core = CoreML()
    score = core.get_score(rezume, llm)

    print("Резюме:", rezume.model_dump())
    print("Скор:", score)

if __name__ == "__main__":
    main()
