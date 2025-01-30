
from flask import jsonify, request
from flask_restful import Resource

from flask_jwt_extended import create_access_token


class LoginController(Resource):
    def post(self):
        input_data = request.get_json()

        email = input_data.get('email')
        password = input_data.get('password')

        registered_user = None

        if not registered_user:
            return jsonify("Invalid Credentials"), 401

        auth_token = create_access_token(identity=str(registered_user.id))

        response = jsonify({
            'user': {
                'id': registered_user.id,
                'email': registered_user.email,
                'avatar': registered_user.avatar
            },
            'authorization_token': auth_token
        })

        response.status_code = 200

        return response

