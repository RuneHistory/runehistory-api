from http import HTTPStatus

from flask import Blueprint, jsonify, abort, Response, request
from ioccontainer import inject
from cmdbus import cmdbus

from runehistory.app.exceptions import DuplicateError, NotFoundError
from runehistory.app.services.account import AccountService
from runehistory.app.commands.account import CreateAccountCommand, \
    GetAccountsCommand, UpdateAccountCommand, GetAccountCommand

accounts_bp = Blueprint('accounts', __name__)


@accounts_bp.route('/<slug>', methods=['GET'])
@inject('account_service')
def get_account(slug, account_service: AccountService) -> Response:
    try:
        account = cmdbus.dispatch(
            GetAccountCommand(account_service, slug)
        )
        return jsonify(account)
    except NotFoundError as e:
        abort(HTTPStatus.NOT_FOUND, str(e))


@accounts_bp.route('', methods=['GET'])
@inject('account_service')
def get_accounts(account_service: AccountService) -> Response:
    last_ran_before = request.args.get('last_ran_before')
    runs_unchanged_min = request.args.get('runs_unchanged_min', type=int)
    runs_unchanged_max = request.args.get('runs_unchanged_max', type=int)
    prioritise = request.args.get('prioritise', False, type=bool)
    accounts = cmdbus.dispatch(GetAccountsCommand(
        account_service, last_ran_before, runs_unchanged_min,
        runs_unchanged_max, prioritise
    ))
    return jsonify(accounts)


@accounts_bp.route('', methods=['POST'])
@inject('account_service')
def post_account(account_service: AccountService) -> Response:
    data = request.get_json()
    try:
        account = cmdbus.dispatch(CreateAccountCommand(
            account_service, data['nickname']
        ))
        return jsonify(account)
    except DuplicateError:
        abort(
            HTTPStatus.BAD_REQUEST,
            'Account already exists: {}'.format(data['nickname'])
        )


@accounts_bp.route('/<slug>', methods=['PUT'])
@inject('account_service')
def put_account(slug, account_service: AccountService) -> Response:
    body = request.get_json()
    try:
        account = cmdbus.dispatch(
            UpdateAccountCommand(account_service, slug, body)
        )
        return jsonify(account)
    except NotFoundError as e:
        abort(HTTPStatus.NOT_FOUND, str(e))
    except ValueError as e:
        abort(HTTPStatus.BAD_REQUEST, str(e))
