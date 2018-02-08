import typing

from flask import Flask, jsonify, Response
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

from ioc import container
from runehistory.framework.services.providers import register_service_providers
from runehistory.framework.api.v1.controllers.accounts import accounts


def make_json_error(ex) -> Response:
    response = jsonify(message=str(ex))
    response.status_code = (ex.code
                            if isinstance(ex, HTTPException)
                            else 500)
    return response


def _json_error_handlers(app: Flask):
    for code in default_exceptions.keys():
        app.register_error_handler(code, make_json_error)


def _register_blueprints(app: Flask):
    app.register_blueprint(accounts, url_prefix='/v1/accounts')


def make_app(import_name: str, **kwargs: typing.Dict) -> Flask:
    app = Flask(import_name, **kwargs)
    app.container = container
    _json_error_handlers(app)
    register_service_providers()
    _register_blueprints(app)

    return app
