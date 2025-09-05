import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

API_KEY = os.getenv("API_KEY")
DB_URL = os.getenv("DB_URL")
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

CONFIG = {
    "API_KEY": API_KEY,
    "DB_URL": DB_URL,
    "DEBUG": DEBUG,
}
