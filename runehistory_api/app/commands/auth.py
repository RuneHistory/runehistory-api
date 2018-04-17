from cmdbus import Command
from evntbus import evntbus
from ioccontainer import inject

from runehistory_api.domain.models.auth import User
from runehistory_api.app.services.auth import JwtService, UserService
from runehistory_api.app.events.auth import JwtCreatedEvent


class CreateJwtCommand(Command):
    @inject('jwt_service')
    def __init__(self, user: User, jwt_service: JwtService):
        self.user = user
        self.jwt_service = jwt_service

    def handle(self):
        jwt = self.jwt_service.make(self.user)
        token = jwt.encode()
        evntbus.emit(JwtCreatedEvent(jwt))
        return token


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
