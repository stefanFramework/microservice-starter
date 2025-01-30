import logging

from functools import wraps
from flask import g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_restful import abort

logger = logging.getLogger(__name__)


def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            g.current_user = current_user
            return fn(*args, **kwargs)
        except Exception as ex:
            logger.exception(ex)
            abort(401, message="Unable to authorize request")
    return wrapper
