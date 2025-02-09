from flask import Flask
from flask_cors import CORS

from flask_restful import Api
from flask_jwt_extended import JWTManager

from app.extensions import db
from app.api.controllers.utils import UtilsController
from app.api.controllers.login import LoginController
from app.api.controllers.books import BooksController


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
    JWTManager(app)
    db.init_app(app)

    return app


def create_api(app):
    api = Api(app)
    api.add_resource(UtilsController, '/health')
    api.add_resource(LoginController, '/login')
    api.add_resource(BooksController, '/books', '/books/<int:book_id>')

    return api
