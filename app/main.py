import logging

from logs import LogConfigurator

from flask import Flask

app = Flask(__name__)

log_config = LogConfigurator()

logger = logging.getLogger()
logger.setLevel(log_config.get_current_log_level())
logger.addHandler(log_config.create_file_handler())
logger.addHandler(log_config.create_console_handler())

if __name__ == '__main__':
    app.run(
        debug=True,  # current_config.DEBUG,
        host='0.0.0.0',
        port=5000
    )
