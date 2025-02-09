import logging

from app.factory import create_app
from app.config import current_config, log_config


app = create_app(current_config)

logger = logging.getLogger()
logger.setLevel(log_config.get_current_log_level())
logger.addHandler(log_config.create_file_handler())
logger.addHandler(log_config.create_console_handler())

if __name__ == '__main__':
    app.run(
        debug=current_config.DEBUG,
        host='0.0.0.0',
        port=5000
    )
