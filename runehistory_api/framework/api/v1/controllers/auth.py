from http import HTTPStatus

from flask import Blueprint, jsonify, abort, Response
from cmdbus import cmdbus
from simplejwt.jwt import Jwt

from runehistory_api.app.commands.auth import CreateJwtCommand
from runehistory_api.framework.auth import requires_auth, user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/token', methods=['GET'])
@requires_auth
def authenticate() -> Response:
    try:
        jwt = cmdbus.dispatch(CreateJwtCommand(user()))  # type: Jwt
        return jsonify({
            'token': jwt.encode()
        })
    except ValueError as e:
        abort(HTTPStatus.BAD_REQUEST, str(e))
