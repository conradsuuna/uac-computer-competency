from os import environ
import psycopg2
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    """ app configuration class """
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = environ.get('SECRET_KEY')

    USER = environ.get('DB_USER')
    PASSWORD = environ.get('DB_PASSWORD')
    DB_NAME = environ.get('DB_NAME')
    HOST = environ.get('DB_HOST')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # jwt configuarations for the user auth api
    JWT_SECRET_KEY = environ.get('SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

    # pagination
    NUM_OF_ITEMS_PER_PAGE = 18

class DevelopmentConfig(Config):
    """ app development configuration class """
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
