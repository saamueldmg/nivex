import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        SQLALCHEMY_DATABASE_URI = database_url.replace("postgres://", "postgresql://", 1)
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'nivex.sqlite'}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = os.getenv("FLASK_ENV") != "production"