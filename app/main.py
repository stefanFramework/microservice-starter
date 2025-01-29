import logging

from flask import Flask

app = Flask(__name__)

# log_configurator = LogConfigurator(current_config)
#
# handlers = [
#     log_configurator.create_file_handler(),
#     log_configurator.create_console_handler()
# ]
#
# logging.basicConfig(
#     handlers=handlers,
#     level=log_configurator.get_current_log_level()
# )

if __name__ == '__main__':
    app.run(
        debug=True,  # current_config.DEBUG,
        host='0.0.0.0',
        port=5000
    )
