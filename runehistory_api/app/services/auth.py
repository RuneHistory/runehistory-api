import typing
from datetime import datetime, timedelta

from ioccontainer import provider, inject
from simplejwt.jwt import Jwt
from passlib.hash import argon2

from runehistory_api.domain.models.auth import User
from runehistory_api.app.repositories.auth import UserRepository
from runehistory_api.app.config import Config


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create(self, username: str, password: str, type: str) -> User:
        hashed_password = argon2.hash(password)
        user = User(username, hashed_password, type)
        return self.user_repository.create(user)

    def find_one_by_id(self, id: str) -> typing.Union[User, None]:
        return self.find_one([['id', id]])

    def find_one_by_username(self, username: str) -> typing.Union[User, None]:
        return self.find_one([['username', username]])

    def find_one(self, where: typing.List = None, fields: typing.List = None) \
            -> typing.Union[User, None]:
        return self.user_repository.find_one(where, fields)

    def validate_password(self, user: User, password: str) -> bool:
        return argon2.verify(password, user.password)


class PermissionService:
    def generate(self, user: User) -> typing.Dict:
        if user.type == 'service':
            return {
                'accounts': ['r', 'c', 'u', 'd'],
                'highscores': ['r', 'c', 'u', 'd'],
                'users': ['r', 'c', 'u', 'd'],
            }
        if user.type == 'guest':
            return {
                'accounts': ['r', 'c'],
                'highscores': ['r'],
            }
        raise ValueError('Unknown user type: {}'.format(user.type))

    def check_permission(self, scope: str, permissions: dict,
                         required: str) -> bool:
        scope_perms = permissions.get(scope, None)
        if not scope_perms:
            return False
        if '*' not in scope_perms and required not in scope_perms:
            return False
        return True


class JwtService:
    @inject('permission_service')
    def __init__(self, secret: str, permission_service: PermissionService):
        self.secret = secret
        self.permission_service = permission_service

    def make(self, user: User) -> Jwt:
        permissions = self.permission_service.generate(user)

        now = datetime.utcnow()
        now_ts = int(now.timestamp())
        expires = now + timedelta(minutes=10)
        expires_ts = int(expires.timestamp())
        jwt = Jwt(
            self.secret,
            {
                'aut': permissions
            },
            issuer='rh-api',
            subject=user.id,
            issued_at=now_ts,
            valid_from=now_ts,
            valid_to=expires_ts
        )
        return jwt

    def decode(self, token: str) -> Jwt:
        return Jwt.decode(self.secret, token)


@provider(UserService)
@inject('repo')
def provide_user_service(repo: UserRepository) -> UserService:
    return UserService(repo)


@provider(PermissionService)
def provide_permission_service() -> PermissionService:
    return PermissionService()


@provider(JwtService)
@inject('config')
def provide_jwt_service(config: Config) -> JwtService:
    return JwtService(config.secret)
