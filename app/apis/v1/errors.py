from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

from app.apis.v1 import api_v1


def api_abort(code, message=None, **kwargs):
    if message is None:
        message = HTTP_STATUS_CODES.get(code, '')

    response = jsonify(code=code, message=message, **kwargs)
    response.status_code = code
    return response


def invalid_token():
    response = api_abort(401, error="invalid_token", error_description="The token is expired or invalid.")
    response.headers["WWW-authenticate"] = "Bearer"
    return response


def token_missing():
    response = api_abort(401)
    response.headers["WWW-authenticated"] = "Bearer"
    return response


class ValidationError(ValueError):
    pass


@api_v1.errorhandler(ValidationError)
def validation_error(e):
    return api_abort(400, e.args[0])