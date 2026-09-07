import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "backend" / "data"
STORAGE_DIR = BASE_DIR / "backend" / "storage"

# Create storage dir if it doesn't exist
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# Settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
DATABASE_PATH = STORAGE_DIR / "careertwin.db"
APP_PORT = int(os.getenv("PORT", 8000))
APP_HOST = os.getenv("HOST", "127.0.0.1")
