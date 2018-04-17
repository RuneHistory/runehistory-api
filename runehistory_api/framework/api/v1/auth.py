from functools import wraps

from flask import request, g
from werkzeug.exceptions import Unauthorized
from cmdbus import cmdbus

from runehistory_api.domain.models.auth import User
from runehistory_api.app.commands.auth import GetUserCommand,\
    ValidateUserPasswordCommand


def check_auth(username, password):
    auth_user = cmdbus.dispatch(GetUserCommand(username))
    is_valid = cmdbus.dispatch(ValidateUserPasswordCommand(
        auth_user,
        password
    ))
    return auth_user if is_valid else None


def user() -> User:
    return g.user


def authenticate():
    # TODO: Send WWW-Authenticate header:
    # 'WWW-Authenticate': 'Basic realm="Login Required"'
    raise Unauthorized('Unauthorized')


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        auth_user = None
        if auth:
            auth_user = check_auth(auth.username, auth.password)
        if not auth_user:
            return authenticate()
        g.user = auth_user
        return f(*args, **kwargs)

    return decorated
