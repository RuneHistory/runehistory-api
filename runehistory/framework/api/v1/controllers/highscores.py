from http import HTTPStatus

from flask import Blueprint, jsonify, abort, Response, request
from cmdbus import cmdbus

from runehistory.app.commands.highscore import CreateHighScoreCommand, \
    GetHighScoreCommand, GetHighScoresCommand
from runehistory.app.exceptions import NotFoundError

highscores_bp = Blueprint('highscores', __name__)


@highscores_bp.route('', methods=['POST'])
def post_highscore(slug: str) -> Response:
    data = request.get_json()
    try:
        highscore = cmdbus.dispatch(CreateHighScoreCommand(
            slug, data['skills']
        ))
        return jsonify(highscore)
    except NotFoundError as e:
        abort(HTTPStatus.NOT_FOUND, str(e))
    except ValueError as e:
        abort(HTTPStatus.BAD_REQUEST, str(e))


@highscores_bp.route('/<id>', methods=['GET'])
def get_highscore(slug: str, id: str) -> Response:
    try:
        highscore = cmdbus.dispatch(GetHighScoreCommand(
            slug, id
        ))
        return jsonify(highscore)
    except NotFoundError as e:
        abort(HTTPStatus.NOT_FOUND, str(e))
    except ValueError as e:
        abort(HTTPStatus.BAD_REQUEST, str(e))


@highscores_bp.route('', methods=['GET'])
def get_highscores(slug: str) -> Response:
    created_after = request.args.get('created_after')
    created_before = request.args.get('created_before')
    skills = request.args.get('skills')
    if skills:
        skills = skills.split(',')
    try:
        highscores = cmdbus.dispatch(GetHighScoresCommand(
            slug, created_after, created_before, skills
        ))
        return jsonify(highscores)
    except ValueError as e:
        abort(HTTPStatus.BAD_REQUEST, str(e))
