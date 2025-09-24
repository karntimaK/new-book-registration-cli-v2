import os
from pathlib import Path

class Settings:
    DATA_PATH: Path = Path(os.getenv("DATA_PATH", "./backend/app/infra/storage/books.json")).resolve()
    CORS_ALLOW_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:5173").split(",")

settings = Settings()
