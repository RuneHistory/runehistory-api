from http import HTTPStatus

from flask import Blueprint, jsonify, abort, Response, request
from ioccontainer import inject

from runehistory.app.exceptions import DuplicateError
from runehistory.framework.services.account import AccountService

accounts = Blueprint('account', __name__, url_prefix='/accounts')


@accounts.route('/<slug>', methods=['GET'])
@inject('account_service')
def get_account(slug, account_service: AccountService) -> Response:
    account = account_service.get(slug)
    if not account:
        abort(HTTPStatus.NOT_FOUND, 'Account not found: {}'.format(slug))
    return jsonify(account.__dict__)


@accounts.route('', methods=['POST'])
@inject('account_service')
def post_account(account_service: AccountService) -> Response:
    data = request.get_json()
    try:
        account = account_service.create(data['nickname'])
        return jsonify(account.__dict__)
    except DuplicateError:
        abort(HTTPStatus.BAD_REQUEST, 'Account already exists: {}'.format(data['nickname']))
