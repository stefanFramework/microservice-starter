import datetime
from flask import jsonify
from flask_restful import Resource

from config import current_config


class UtilsController(Resource):
    def get(self):
        current_date = datetime.datetime.now()
        response = jsonify({
            'name': current_config.NAME,
            'version': '1.0.0',
            'date': current_date.strftime("%Y-%m-%d %H:%M")
        })

        response.status_code = 200
        return response
