import os

from enum import Enum
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv('.env')


class EnvironmentTypes(str, Enum):
    DEVELOPMENT = 'development'
    STAGING = 'staging'
    PRODUCTION = 'production'


class BaseConfig:
    DEBUG = False

    NAME = os.getenv('NAME', 'microservice-starter')

    # When set tu True, it ignores middleware authentication
    SKIP_AUTH = os.getenv('SKIP_AUTH', False)

    # Multiple language support
    LOCALE = os.getenv('LOCALE', 'es')

    BASE_URL = os.getenv('BASE_URL')

    # For CORS purposes
    FRONTEND_URL = os.getenv('FRONTEND_URL')

    ENVIRONMENT = EnvironmentTypes.DEVELOPMENT

    # Track inserts, updates, and deletes for models. Signals before or during session.flush() and session.commit()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Ex: postgresql://<user>:<pass>@<host>:<port>/<database>
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    # The number of connections to keep open inside the connection pool
    SQLALCHEMY_DATABASE_POOL_SIZE = 5

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ALGORITHM = "HS256"
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=6)  # Expires in 6 hours

    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_SECRET_KEY = os.getenv('GOOGLE_SECRET_KEY')


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENVIRONMENT = EnvironmentTypes.DEVELOPMENT


class ProductionConfig(BaseConfig):
    DEBUG = False
    ENVIRONMENT = EnvironmentTypes.PRODUCTION


def get_current_config():
    env = os.getenv('ENVIRONMENT', EnvironmentTypes.DEVELOPMENT)
    if env == EnvironmentTypes.PRODUCTION:
        return ProductionConfig()
    return DevelopmentConfig()


current_config = get_current_config()

