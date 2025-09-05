from __future__ import annotations
from app.config import CONFIG

import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


class LLMCore:
    def __init__(self, *, pool_connections: int = 10, pool_maxsize: int = 50, timeout: float = 10.0):
        self._ENDPOINT = "https://api.proxyapi.ru/google/v1beta/models/gemini-2.0-flash:generateContent"
        # keep-alive по умолчанию включён у requests; явно не вредно
        self._headers = {
            "Authorization": f"Bearer {CONFIG['API_KEY']}",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
        }
        self._timeout = timeout

        # Настраиваем сессию с пулом соединений и ретраями
        self._session = requests.Session()

        retries = Retry(
            total=3,
            backoff_factor=0.3,                # экспоненциальная задержка: 0.3, 0.6, 1.2 …
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(["POST"]),
            raise_on_status=False,
            respect_retry_after_header=True,
        )

        adapter = HTTPAdapter(
            pool_connections=pool_connections,
            pool_maxsize=pool_maxsize,
            max_retries=retries,
        )

        # HTTP и HTTPS — один и тот же адаптер
        self._session.mount("http://", adapter)
        self._session.mount("https://", adapter)

    def __del__(self):
        # закроем сессию при сборке мусора (на всякий). Лучше вызывать явно .close()
        try:
            self._session.close()
        except Exception:
            pass

    def close(self):
        """Явное закрытие сессии, если нужно."""
        self._session.close()

    def _call_gemini(self, system_prompt: str, user_text: str, GENCFG: dict | None = None):
        # Подготовим payload один раз как str -> экономим на encode в urllib3
        payload = json.dumps({
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"parts": [{"text": user_text}]}],
            "generationConfig": GENCFG,
        }, ensure_ascii=False)

        try:
            # Используем persistent-сессию и соединение из пула
            resp = self._session.post(
                self._ENDPOINT,
                headers=self._headers,
                data=payload,           # data со строкой быстрее, чем json= (меньше работы на сериализацию)
                timeout=self._timeout,
            )
            # Если пришёл ретраябельный код — Retry в адаптере уже попробовал сам
            resp.raise_for_status()
        except requests.RequestException:
            return None

        try:
            data = resp.json()
            parts = data["candidates"][0]["content"]["parts"]
            text = "".join(p.get("text", "") for p in parts if isinstance(p, dict)).strip()
        except Exception:
            return None

        return text