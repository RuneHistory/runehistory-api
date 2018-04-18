from functools import wraps

from flask import request, g
from werkzeug.exceptions import Unauthorized
from cmdbus import cmdbus
from simplejwt.jwt import Jwt
from simplejwt.exception import InvalidTokenError

from runehistory_api.domain.models.auth import User
from runehistory_api.app.commands.auth import GetUserCommand,\
    ValidateUserPasswordCommand, DecodeJwtCommand, GetUserByIdCommand


def check_auth(username: str, password: str):
    auth_user = cmdbus.dispatch(GetUserCommand(username))
    is_valid = cmdbus.dispatch(ValidateUserPasswordCommand(
        auth_user,
        password
    ))
    return auth_user if is_valid else None


def check_jwt(token: str):
    try:
        jwt = cmdbus.dispatch(DecodeJwtCommand(token))  # type: Jwt
    except InvalidTokenError:
        return None
    if not jwt.valid():
        return None
    return cmdbus.dispatch(GetUserByIdCommand(jwt.subject))


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


def requires_jwt(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise Unauthorized('Missing Authorization Header')

        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != 'Bearer':
            raise Unauthorized('Invalid Authorization Header')

        token = parts[1]
        auth_user = check_jwt(token)
        if not auth_user:
            raise Unauthorized('Invalid token')
        g.user = auth_user
        return f(*args, **kwargs)

    return decorated
