import os
from dotenv import load_dotenv

load_dotenv()

class Development():
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class Production():
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']

class Testing():
    """
    Testing environment configurations
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

app_config = {
    'development': Development,
    'production': Production,
    'testing': Testing,
}