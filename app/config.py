import os
import sys
import json
import logging

from os.path import join
from enum import Enum
from datetime import timedelta, datetime
from dotenv import load_dotenv

from logging.handlers import TimedRotatingFileHandler
from pythonjsonlogger.jsonlogger import JsonFormatter

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

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'M1CR0S3RV1C3')
    JWT_ALGORITHM = "HS256"
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=6)  # Expires in 6 hours
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=3)  # Expires in 3 days

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


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class LogConfigurator:
    DEFAULT_LOG_FILE_FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s %(pathname)s %(lineno)d %(module)s %(funcName)s'
    DEFAULT_LOG_CONSOLE_FORMAT = '[%(asctime)s] (%(name)s) %(levelname)s: %(message)s'

    def __init__(self):
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

        self.LOG_FILENAME = join('storage/logs', os.getenv('LOG_FILENAME', 'mss.log'))
        self.LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 7))
        self.LOG_ROTATION_INTERVAL = int(os.getenv('LOG_ROTATION_INTERVAL', 1))
        self.LOG_ROTATION_INTERVAL_UNIT = os.getenv('LOG_ROTATION_INTERVAL_UNIT', 'D')

        self.LOG_FILE_FORMAT = os.getenv('LOG_FILE_FORMAT', self.DEFAULT_LOG_FILE_FORMAT)
        self.LOG_CONSOLE_FORMAT = os.getenv('LOG_CONSOLE_FORMAT', self.DEFAULT_LOG_CONSOLE_FORMAT)

    def create_file_handler(self):
        handler = TimedRotatingFileHandler(
            filename=self.LOG_FILENAME,
            when=self.LOG_ROTATION_INTERVAL_UNIT,
            backupCount=self.LOG_BACKUP_COUNT,
            interval=self.LOG_ROTATION_INTERVAL,
            encoding='utf-8'
        )
        formatter = JsonFormatter(fmt=self.LOG_FILE_FORMAT, json_encoder=CustomJsonEncoder)
        handler.setFormatter(formatter)
        return handler

    def create_console_handler(self):
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(fmt=self.LOG_CONSOLE_FORMAT)
        handler.setFormatter(formatter)
        return handler

    def get_current_log_level(self):
        return self.LOG_LEVEL


log_config = LogConfigurator()

