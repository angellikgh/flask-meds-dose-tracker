import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """Base config, uses staging database server."""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Database Configs
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True

