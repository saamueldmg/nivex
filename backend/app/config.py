import os
from datetime import timedelta

class Config:
    # Base de datos SQLite para desarrollo
    SQLALCHEMY_DATABASE_URI = 'sqlite:///nivex.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'nivex-secret-key-2026')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    # Seguridad
    SECRET_KEY = os.environ.get('SECRET_KEY', 'nivex-flask-secret-2026')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///nivex.db')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}