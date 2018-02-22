from http import HTTPStatus

from flask import Blueprint, jsonify, abort, Response, request
from ioccontainer import inject
from cmdbus import cmdbus

from runehistory.app.services.account import AccountService
from runehistory.app.services.highscore import HighScoreService
from runehistory.app.commands.highscore import CreateHighScoreCommand, \
    GetHighScoreCommand
from runehistory.app.exceptions import NotFoundError

highscores_bp = Blueprint('highscores', __name__)


@highscores_bp.route('', methods=['POST'])
@inject('account_service', 'highscore_service')
def post_highscore(slug: str, account_service: AccountService,
                   highscore_service: HighScoreService) -> Response:
    data = request.get_json()
    try:
        highscore = cmdbus.dispatch(CreateHighScoreCommand(
            account_service, highscore_service, slug, data['skills']
        ))
        return jsonify(highscore)
    except NotFoundError as e:
        abort(HTTPStatus.NOT_FOUND, str(e))
    except ValueError as e:
        abort(HTTPStatus.BAD_REQUEST, str(e))


@highscores_bp.route('/<id>', methods=['GET'])
@inject('account_service', 'highscore_service')
def get_highscore(slug: str, id: str, account_service: AccountService,
                  highscore_service: HighScoreService) -> Response:
    try:
        highscore = cmdbus.dispatch(GetHighScoreCommand(
            account_service, highscore_service, slug, id
        ))
        return jsonify(highscore)
    except NotFoundError as e:
        abort(HTTPStatus.NOT_FOUND, str(e))
    except ValueError as e:
        abort(HTTPStatus.BAD_REQUEST, str(e))
