import os

class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_AVATARS_DEST = 'static/img/uploads'
    SECRET_KEY = 'watchlist'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///db/{os.getenv("DATABASE_FILE", "data.db")}'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/data.db'
    DEBUG = True
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'


class TestingConfig(Config):
    TESTING = True
