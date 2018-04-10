from evntbus import Event
from simplejwt.jwt import Jwt


class JwtCreatedEvent(Event):
    def __init__(self, jwt: Jwt):
        self.jwt = jwt
