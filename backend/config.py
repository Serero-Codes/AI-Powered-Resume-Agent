import os
from pathlib import Path
from dotenv import load_dotenv

# Identify the backend directory
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from backend/.env
load_dotenv(BASE_DIR / ".env")

# Directory containing application data
DATA_DIR = BASE_DIR / "data"

# Permanent career profile location
PROFILE_PATH = DATA_DIR / "career_profile.json"

# Flask configuration
FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)