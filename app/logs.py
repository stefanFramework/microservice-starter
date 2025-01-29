import sys
import json
import logging
import os

from os.path import join
from datetime import datetime
from dotenv import load_dotenv
from logging.handlers import TimedRotatingFileHandler
from pythonjsonlogger.jsonlogger import JsonFormatter

load_dotenv('.env')


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

        self.LOG_FILENAME = join('logs', os.getenv('LOG_FILENAME', 'mss.log'))
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
