from .GeminiClient import GeminiClient
from .prompts.fio import FIO_PROMPT
from app.domain.models import FIOResult, NameParts



class LLM(GeminiClient):
    
    def checking_FIO(self, data: NameParts) -> FIOResult:
        GENCFG = {
            "candidateCount": 1,
            "maxOutputTokens": 3,
            "temperature": 0.0,
            "topP": 1.0,
            "seed": 0,
            "responseMimeType": "text/plain",
        }
        response = self._call_gemini(FIO_PROMPT, str(data), GENCFG=GENCFG)
        if response is None:
            return FIOResult("000")
        return FIOResult(response)

    def analysis_of_legend(self, text: str, patterns: dict[int, str]) -> int:
        # Анализ легенды резюме на предмет накрутки (мок — 1)
        return 1

_llm = LLM()


def get_llm() -> LLM:
    return _llm