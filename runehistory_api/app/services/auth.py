import typing
from datetime import datetime, timedelta

from ioccontainer import provider, inject
from simplejwt.jwt import Jwt


class PermissionService:
    # Todo: User instead of type
    def generate(self, user_type: str) -> typing.Dict:
        if user_type == 'service':
            return {
                'account': ['r', 'c', 'u', 'd'],
                'highscore': ['r', 'c', 'u', 'd'],
            }
        if user_type == 'guest':
            return {
                'account': ['r'],
                'highscore': ['r'],
            }
        raise ValueError('Unknown user type: {}'.format(user_type))


class JwtService:
    @inject('permission_service')
    def __init__(self, permission_service: PermissionService):
        self.permission_service = permission_service

    def make(self, user_type: str) -> Jwt:  # Todo: User instead of type
        permissions = self.permission_service.generate(user_type)

        secret = 'abc'  # TODO: Load from config
        now = datetime.utcnow()
        now_ts = int(now.timestamp())
        expires = now + timedelta(minutes=30)
        expires_ts = int(expires.timestamp())
        jwt = Jwt(
            secret,
            {
                'aut': permissions
            },
            issuer='rh-api',
            subject='user-id',
            issued_at=now_ts,
            valid_from=now_ts,
            valid_to=expires_ts
        )
        return jwt


@provider(PermissionService)
def provide_permission_service() -> PermissionService:
    return PermissionService()


@provider(JwtService)
def provide_jwt_service() -> JwtService:
    return JwtService()
