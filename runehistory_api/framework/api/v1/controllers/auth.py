from http import HTTPStatus

from flask import Blueprint, jsonify, abort, Response
from cmdbus import cmdbus

from runehistory_api.app.commands.auth import CreateJwtCommand

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/authenticate', methods=['POST'])
def get_account() -> Response:
    """
    Authenticate user with:
     - username
     - password

    User types
      - service
      - guest for UI?

    Users
      - type (service)
      - username (rh-cli)
      - password (some random api key)

    1. Client gets token string and stores it in session/cookie
    2. Every request from then on WITH this in the session will include "Authorization: Bearer {token}" header
    3. API validates the jwt
    4. API validates permissions in the jwt
    5. API processes request

    """
    try:
        # TODO: Get user making request and validate api key.
        # TODO: Pass user to command.
        token = cmdbus.dispatch(CreateJwtCommand())
        return jsonify({
            'token': token
        })
    except ValueError as e:
        abort(HTTPStatus.BAD_REQUEST, str(e))
