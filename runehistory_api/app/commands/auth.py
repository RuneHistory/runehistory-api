from cmdbus import Command
from evntbus import evntbus
from ioccontainer import inject

from runehistory_api.app.services.auth import JwtService
from runehistory_api.app.events.auth import JwtCreatedEvent


class CreateJwtCommand(Command):
    @inject('jwt_service')
    def __init__(self, jwt_service: JwtService):
        self.jwt_service = jwt_service

    def handle(self):
        # TODO: Pass user instead of type
        jwt = self.jwt_service.make('service')
        token = jwt.encode()
        evntbus.emit(JwtCreatedEvent(jwt))
        return token
