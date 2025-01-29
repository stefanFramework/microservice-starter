from flask import Flask
from flask_cors import CORS

from flask_restful import Api

from api.controllers.utils import UtilsController


def create_app(current_config):
    app = Flask(current_config.NAME)
    app.config.from_object(current_config)

    CORS(app, resources={r"/*": {
        "origins": current_config.FRONTEND_URL,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Authorization", "Content-Type"],
        "supports_credentials": True,
    }})

    @app.after_request
    def add_coop_and_coep_headers(response):
        response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
        response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
        return response

    create_api(app)
    # AuthorizationMiddleware(app)
    # JWTManager(app)
    # db.init_app(app)

    return app


def create_api(app):
    api = Api(app)
    api.add_resource(UtilsController, '/health')

    # app.register_error_handler(AuthorizationTokenError, handle_authorization_token_error)
    # app.register_error_handler(FieldValidationError, handle_validation_error)
    # app.register_error_handler(UserSuspendedError, handle_invalid_user_error)
    # app.register_error_handler(Exception, handle_server_error)
    return api
