from cmdbus import Command, cmdbus
from evntbus import evntbus
from ioccontainer import inject

from runehistory_api.domain.models.auth import User
from runehistory_api.app.services.auth import JwtService, UserService, \
    PermissionService
from runehistory_api.app.events.auth import JwtCreatedEvent


class CreateJwtCommand(Command):
    @inject('jwt_service')
    def __init__(self, user: User, jwt_service: JwtService):
        self.user = user
        self.jwt_service = jwt_service

    def handle(self):
        jwt = self.jwt_service.make(self.user)
        evntbus.emit(JwtCreatedEvent(jwt))
        return jwt


class DecodeJwtCommand(Command):
    @inject('jwt_service')
    def __init__(self, token: str, jwt_service: JwtService):
        self.token = token
        self.jwt_service = jwt_service

    def handle(self):
        return self.jwt_service.decode(self.token)


class CreateUserCommand(Command):
    @inject('user_service')
    def __init__(self, username: str, password: str, type: str,
                 user_service: UserService):
        self.username = username
        self.password = password
        self.type = type
        self.user_service = user_service

    def handle(self):
        return self.user_service.create(self.username, self.password,
                                        self.type)


class GetUserByIdCommand(Command):
    @inject('user_service')
    def __init__(self, id: str, user_service: UserService):
        self.id = id
        self.user_service = user_service

    def handle(self):
        return self.user_service.find_one_by_id(self.id)


class GetUserCommand(Command):
    @inject('user_service')
    def __init__(self, username: str, user_service: UserService):
        self.username = username
        self.user_service = user_service

    def handle(self):
        return self.user_service.find_one_by_username(self.username)


class ValidateUserPasswordCommand(Command):
    @inject('user_service')
    def __init__(self, user: User, password: str, user_service: UserService):
        self.user = user
        self.password = password
        self.user_service = user_service

    def handle(self):
        return self.user_service.validate_password(self.user, self.password)


class GeneratePermissionsCommand(Command):
    @inject('permission_service')
    def __init__(self, user: User, permission_service: PermissionService):
        self.user = user
        self.permission_service = permission_service

    def handle(self):
        return self.permission_service.generate(self.user)


class CheckPermissionCommand(Command):
    @inject('permission_service')
    def __init__(self, scope: str, permissions: dict, required: str,
                 permission_service: PermissionService):
        self.scope = scope
        self.permissions = permissions
        self.required = required
        self.permission_service = permission_service

    def handle(self):
        return self.permission_service.check_permission(
            self.scope,
            self.permissions,
            self.required
        )


class CheckUserPermissionCommand(Command):
    @inject('permission_service')
    def __init__(self, user: User, scope: str, required: str):
        self.user = user
        self.scope = scope
        self.required = required

    def handle(self):
        permissions = cmdbus.dispatch(GeneratePermissionsCommand(self.user))
        return cmdbus.dispatch(
            CheckPermissionCommand(self.scope, permissions, self.required)
        )
