from flask import Blueprint, jsonify, Response
from cmdbus import cmdbus

from runehistory_api.app.commands.stats import GetAccountCountCommand, \
    GetHighScoreCountCommand
from runehistory_api.framework.auth import requires_jwt, requires_permission

stats_bp = Blueprint('stats', __name__)


@stats_bp.route('/accounts/count', methods=['GET'])
@requires_jwt
@requires_permission('accounts', 'r')
def get_account_count() -> Response:
    count = cmdbus.dispatch(
        GetAccountCountCommand()
    )
    return jsonify(count)


@stats_bp.route('/highscores/count', methods=['GET'])
@requires_jwt
@requires_permission('highscores', 'r')
def get_highscore_count() -> Response:
    count = cmdbus.dispatch(
        GetHighScoreCountCommand()
    )
    return jsonify(count)
