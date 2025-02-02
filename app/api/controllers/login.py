from flask import g, jsonify, request, make_response
from flask_restful import Resource

from flask_jwt_extended import create_access_token

from models import User


class LoginController(Resource):
    def post(self):
        input_data = request.get_json()

        email = input_data.get('email')
        password = input_data.get('password')

        registered_user = User.query.filter_by(email=email).one_or_none()

        if (not registered_user or
                not registered_user.check_password(password)):
            return jsonify("Invalid Credentials"), 401

        auth_token = create_access_token(identity=str(registered_user.id))

        response = jsonify({
            'user': {
                'id': registered_user.id,
                'email': registered_user.email,
                'name': registered_user.name,
                'avatar': registered_user.avatar
            },
            'authorization_token': auth_token
        })

        return make_response(response, 200)



