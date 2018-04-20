import typing
from functools import wraps

from flask import request, g
from werkzeug.exceptions import Unauthorized, Forbidden
from cmdbus import cmdbus
from simplejwt.jwt import Jwt
from simplejwt.exception import InvalidTokenError
from ioccontainer import inject

from runehistory_api.domain.models.auth import User
from runehistory_api.app.commands.auth import GetUserCommand, \
    ValidateUserPasswordCommand, DecodeJwtCommand, GetUserByIdCommand, \
    CreateJwtCommand, CheckUserPermissionCommand
from runehistory_api.app.services.auth import PermissionService


def check_auth(username: str, password: str):
    auth_user = cmdbus.dispatch(GetUserCommand(username))
    is_valid = cmdbus.dispatch(ValidateUserPasswordCommand(
        auth_user,
        password
    ))
    return auth_user if is_valid else None


def check_jwt(token: str) -> typing.Union[Jwt, None]:
    try:
        jwt = cmdbus.dispatch(DecodeJwtCommand(token))  # type: Jwt
    except InvalidTokenError:
        return None
    if not jwt.valid():
        return None
    return jwt


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
        jwt = check_jwt(token)
        if not jwt:
            raise Unauthorized('Invalid token')
        auth_user = cmdbus.dispatch(GetUserByIdCommand(jwt.subject))
        if not auth_user:
            raise Unauthorized('Invalid token')
        new_jwt = cmdbus.dispatch(CreateJwtCommand(auth_user))  # type: Jwt
        if not jwt.compare(new_jwt):
            raise Unauthorized('Invalid token')
        g.jwt = jwt
        g.user = auth_user
        return f(*args, **kwargs)

    return decorated


class RequiresPermissionDecorator:
    @inject('permission_service')
    def __init__(self, scope: str, required: str,
                 permission_service: PermissionService):
        self.scope = scope
        self.required = required
        self.permission_service = permission_service

    def __call__(self, f: typing.Callable) -> typing.Callable:
        @wraps(f)
        def decorated(*args, **kwargs):
            if not cmdbus.dispatch(
                    CheckUserPermissionCommand(
                        user(), self.scope,
                        self.required)
            ):
                raise Forbidden()
            return f(*args, **kwargs)

        return decorated


requires_permission = RequiresPermissionDecorator
