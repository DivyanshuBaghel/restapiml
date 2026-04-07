"""
Application settings loaded from environment variables / .env file.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the rest_api/ directory
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_path)

MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017")
DB_NAME: str = os.getenv("DB_NAME", "mlbb_guide")
