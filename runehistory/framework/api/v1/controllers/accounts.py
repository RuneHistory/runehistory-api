from http import HTTPStatus

from flask import Blueprint, jsonify, abort, Response

from ioccontainer import inject
from runehistory.framework.services.account import AccountService

accounts = Blueprint('account', __name__, url_prefix='/accounts')


@accounts.route('/<slug>', methods=['GET'])
@inject('account_service')
def get_account(slug, account_service: AccountService) -> Response:
    account = account_service.get(slug)
    if not account:
        abort(HTTPStatus.NOT_FOUND, 'Account not found: {}'.format(slug))
    return jsonify(account.__dict__)
