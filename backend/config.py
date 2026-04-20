import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    # Base de datos SQLite en un archivo llamado nivex.sqlite dentro de backend
    SQLALCHEMY_DATABASE_URI = (
        os.getenv(
            "DATABASE_URL",
            f"sqlite:///{BASE_DIR / 'nivex.sqlite'}",
        )
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = True