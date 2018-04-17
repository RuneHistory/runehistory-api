from http import HTTPStatus

from flask import Blueprint, jsonify, abort, Response
from cmdbus import cmdbus

from runehistory_api.app.commands.auth import CreateJwtCommand
from runehistory_api.framework.api.v1.auth import requires_auth, user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/token', methods=['GET'])
@requires_auth
def authenticate() -> Response:
    """
    1. Client gets token string and stores it in session/cookie
    2. Every request from then on WITH this in the session will include "Authorization: Bearer {token}" header
    3. API validates the jwt
    4. API validates permissions in the jwt
    5. API processes request
    """
    try:
        token = cmdbus.dispatch(CreateJwtCommand(user()))
        return jsonify({
            'token': token
        })
    except ValueError as e:
        abort(HTTPStatus.BAD_REQUEST, str(e))
