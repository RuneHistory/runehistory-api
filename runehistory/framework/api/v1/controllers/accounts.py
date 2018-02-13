from http import HTTPStatus
from datetime import datetime

from flask import Blueprint, jsonify, abort, Response, request
from ioccontainer import inject
import dateutil.parser

from runehistory.app.exceptions import DuplicateError
from runehistory.framework.services.account import AccountService

accounts_bp = Blueprint('account', __name__, url_prefix='/accounts')


@accounts_bp.route('/<slug>', methods=['GET'])
@inject('account_service')
def get_account(slug, account_service: AccountService) -> Response:
    account = account_service.find_one(slug)
    if not account:
        abort(HTTPStatus.NOT_FOUND, 'Account not found: {}'.format(slug))
    return jsonify(account)


@accounts_bp.route('', methods=['GET'])
@inject('account_service')
def get_accounts(account_service: AccountService) -> Response:
    last_ran_before = request.args.get('last_ran_before')
    if last_ran_before is not None:
        last_ran_before = dateutil.parser.parse(last_ran_before)
    runs_unchanged_min = request.args.get('runs_unchanged_min')
    if runs_unchanged_min is not None:
        runs_unchanged_min = int(runs_unchanged_min)
    runs_unchanged_max = request.args.get('runs_unchanged_max')
    if runs_unchanged_max is not None:
        runs_unchanged_max = int(runs_unchanged_max)
    prioritise = request.args.get('prioritise', False)
    if prioritise is not False:
        prioritise = bool(prioritise)
    accounts = account_service.find(last_ran_before, runs_unchanged_min,
                                    runs_unchanged_max, prioritise)
    return jsonify(accounts)


@accounts_bp.route('', methods=['POST'])
@inject('account_service')
def post_account(account_service: AccountService) -> Response:
    data = request.get_json()
    try:
        account = account_service.create(data['nickname'])
        return jsonify(account)
    except DuplicateError:
        abort(
            HTTPStatus.BAD_REQUEST,
            'Account already exists: {}'.format(data['nickname'])
        )
