import typing

from flask import Flask, jsonify, Response
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

from runehistory.framework.services.providers import register_service_providers
from runehistory.framework.api.v1.controllers.accounts import accounts_bp
from runehistory.framework.json_encoder import CustomJsonEncoder


def get_json_error_handler(app: Flask):
    def make_json_error(ex) -> Response:
        status_code = (ex.code
                       if isinstance(ex, HTTPException)
                       else 500)
        message = 'Something went wrong'
        if status_code < 500 or app.debug:
            if isinstance(ex, HTTPException):
                message = ex.description
                if message is type(ex).description:
                    message = ex.name
            else:
                message = str(ex)
        response = jsonify(message=message)
        response.status_code = status_code
        return response

    return make_json_error


def _json_error_handlers(app: Flask):
    for code in default_exceptions.keys():
        app.register_error_handler(code, get_json_error_handler(app))


def _register_blueprints(app: Flask):
    app.register_blueprint(accounts_bp, url_prefix='/v1/accounts')


def make_app(import_name: str, **kwargs: typing.Dict) -> Flask:
    app = Flask(import_name, **kwargs)
    _json_error_handlers(app)
    register_service_providers()
    _register_blueprints(app)
    app.json_encoder = CustomJsonEncoder

    return app
