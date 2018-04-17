import typing
from datetime import datetime, timedelta

from ioccontainer import provider, inject
from simplejwt.jwt import Jwt
from passlib.hash import argon2

from runehistory_api.domain.models.auth import User
from runehistory_api.app.repositories.auth import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create(self, username: str, password: str, type: str) -> User:
        hashed_password = argon2.hash(password)
        user = User(username, hashed_password, type)
        return self.user_repository.create(user)

    def find_one_by_username(self, username: str) -> typing.Union[User, None]:
        return self.find_one([['username', username]])

    def find_one(self, where: typing.List = None, fields: typing.List = None)\
            -> typing.Union[User, None]:
        return self.user_repository.find_one(where, fields)

    def validate_password(self, user: User, password: str) -> bool:
        return argon2.verify(password, user.password)


class PermissionService:
    def generate(self, user: User) -> typing.Dict:
        if user.type == 'service':
            return {
                'account': ['r', 'c', 'u', 'd'],
                'highscore': ['r', 'c', 'u', 'd'],
                'user': ['r', 'c', 'u', 'd'],
            }
        if user.type == 'guest':
            return {
                'account': ['r'],
                'highscore': ['r'],
            }
        raise ValueError('Unknown user type: {}'.format(user.type))


class JwtService:
    @inject('permission_service')
    def __init__(self, permission_service: PermissionService):
        self.permission_service = permission_service

    def make(self, user: User) -> Jwt:
        permissions = self.permission_service.generate(user)

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


@provider(UserService)
@inject('repo')
def provide_user_service(repo: UserRepository) -> UserService:
    return UserService(repo)


@provider(PermissionService)
def provide_permission_service() -> PermissionService:
    return PermissionService()


@provider(JwtService)
def provide_jwt_service() -> JwtService:
    return JwtService()
