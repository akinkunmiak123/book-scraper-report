from pathlib import Path

# The folder this file lives in, no matter where Python is launched from
BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"
LOG_DIR = BASE_DIR / "logs"

URL = "https://books.toscrape.com/"
HEADERS = {"User-Agent": "Mozilla/5.0 (learning project)"}

MAX_RETRIES = 3
RETRY_WAIT_SECONDS = 5