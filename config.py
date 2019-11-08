class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/data.db'
    DEBUG = True


class TestingConfig(Config):
    TESTING = True