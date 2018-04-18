from http import HTTPStatus

from flask import Blueprint, jsonify, abort, Response, request
from cmdbus import cmdbus

from runehistory_api.app.exceptions import DuplicateError, NotFoundError
from runehistory_api.app.commands.account import CreateAccountCommand, \
    GetAccountsCommand, UpdateAccountCommand, GetAccountCommand
from runehistory_api.framework.auth import requires_jwt

accounts_bp = Blueprint('accounts', __name__)


@accounts_bp.route('/<slug>', methods=['GET'])
def get_account(slug) -> Response:
    try:
        account = cmdbus.dispatch(
            GetAccountCommand(slug)
        )
        return jsonify(account)
    except NotFoundError as e:
        abort(HTTPStatus.NOT_FOUND, str(e))
    except ValueError as e:
        abort(HTTPStatus.BAD_REQUEST, str(e))


@accounts_bp.route('', methods=['GET'])
@requires_jwt
def get_accounts() -> Response:
    last_ran_before = request.args.get('last_ran_before')
    runs_unchanged_min = request.args.get('runs_unchanged_min', type=int)
    runs_unchanged_max = request.args.get('runs_unchanged_max', type=int)
    prioritise = request.args.get('prioritise', False, type=bool)
    try:
        accounts = cmdbus.dispatch(GetAccountsCommand(
            last_ran_before, runs_unchanged_min,
            runs_unchanged_max, prioritise
        ))
        return jsonify(accounts)
    except ValueError as e:
        abort(HTTPStatus.BAD_REQUEST, str(e))


@accounts_bp.route('', methods=['POST'])
def post_account() -> Response:
    data = request.get_json()
    try:
        account = cmdbus.dispatch(CreateAccountCommand(
            data['nickname']
        ))
        return jsonify(account)
    except DuplicateError:
        abort(
            HTTPStatus.BAD_REQUEST,
            'Account already exists: {}'.format(data['nickname'])
        )
    except ValueError as e:
        abort(HTTPStatus.BAD_REQUEST, str(e))


@accounts_bp.route('/<slug>', methods=['PUT'])
def put_account(slug) -> Response:
    body = request.get_json()
    try:
        account = cmdbus.dispatch(
            UpdateAccountCommand(slug, body)
        )
        return jsonify(account)
    except NotFoundError as e:
        abort(HTTPStatus.NOT_FOUND, str(e))
    except ValueError as e:
        abort(HTTPStatus.BAD_REQUEST, str(e))
