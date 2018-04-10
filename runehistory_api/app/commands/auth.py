import typing
from datetime import datetime, timedelta

from cmdbus import Command
from evntbus import evntbus
from simplejwt.jwt import Jwt

from runehistory_api.app.events.auth import JwtCreatedEvent


class CreateJwtCommand(Command):
    def __init__(self):
        pass

    def handle(self):
        """
        TODO:
        1. Find the type of the user
        2. Generate some permissions based on user type + specific user
        3. Create + return token
        """
        secret = 'abc'
        now = datetime.utcnow()
        now_ts = int(now.timestamp())
        expires = now + timedelta(minutes=30)
        expires_ts = int(expires.timestamp())
        jwt = Jwt(
            secret,
            {
                'aut': {}  # Permissions
            },
            issuer='rh-api',
            subject='user-id',
            issued_at=now_ts,
            valid_from=now_ts,
            valid_to=expires_ts
        )
        token = jwt.encode()
        evntbus.emit(JwtCreatedEvent(jwt))
        return token
