from pathlib import Path

from dotenv import load_dotenv
import os

# Загрузка переменных из .env файла
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

report_path: Path = Path(os.getenv("REPORT_PATH"))
