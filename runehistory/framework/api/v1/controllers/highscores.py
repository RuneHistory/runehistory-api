from http import HTTPStatus

from flask import Blueprint, jsonify, abort, Response, request
from ioccontainer import inject

from runehistory.framework.services.account import AccountService
from runehistory.framework.services.highscore import HighScoreService

highscores_bp = Blueprint('highscores', __name__)


@highscores_bp.route('', methods=['POST'])
@inject('account_service', 'highscore_service')
def post_highscore(slug: str, account_service: AccountService,
                   highscore_service: HighScoreService) -> Response:
    account = account_service.find_one_by_slug(slug)
    data = request.get_json()
    if not account:
        abort(HTTPStatus.NOT_FOUND, 'Account not found: {}'.format(slug))
    highscore = highscore_service.create(account, data['skills'])
    return jsonify(highscore)


@highscores_bp.route('/<id>', methods=['GET'])
@inject('account_service', 'highscore_service')
def get_highscore(slug: str, id: str, account_service: AccountService,
                  highscore_service: HighScoreService) -> Response:
    account = account_service.find_one_by_slug(slug)
    if not account:
        abort(HTTPStatus.NOT_FOUND, 'Account not found: {}'.format(slug))
    highscore = highscore_service.find_one_by_account(account.id, id)
    if not highscore:
        abort(HTTPStatus.NOT_FOUND, 'Highscore not found: {}'.format(id))
    return jsonify(highscore)
