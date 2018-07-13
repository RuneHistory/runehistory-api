import typing
from datetime import datetime

from ioccontainer import provider, inject

from runehistory_api.app.database import DatabaseAdapter, TableAdapter
from runehistory_api.domain.models.auth import User


class UserRepository:
    id = 'id'
    ids = []

    def __init__(self, users: TableAdapter):
        self.users = users
        self.users.id = type(self).id
        self.users.ids = type(self).ids

    def create(self, user: User) -> User:
        if user.created_at is None:
            user.created_at = datetime.utcnow()
        record = self.users.insert(UserRepository.to_record(user))
        return UserRepository.from_record(record)

    def find_one(self, where: typing.List = None, fields: typing.List = None) \
            -> typing.Union[User, None]:
        record = self.users.find_one(where, fields)
        if record is None:
            return None
        return UserRepository.from_record(record)

    def find(self, where: typing.List = None, fields: typing.List = None,
             limit: int = None, offset: int = None,
             order: typing.List = None
             ) -> typing.List:
        results = self.users.find(where, fields, limit, offset, order)
        return [user for user in
                map(UserRepository.from_record, results)]

    def update_one(self, where: typing.List, data: typing.Dict) -> bool:
        return self.users.update_one(where, data)

    def update(self, user: User, data: typing.Dict) -> bool:
        user_id = getattr(user, type(self).id, None)
        if not user_id:
            return False
        data['updated_at'] = datetime.utcnow()
        old_data = dict()
        for k, v in data.items():
            old_data[k] = getattr(user, k)
            setattr(user, k, v)
        updated = self.update_one([[type(self).id, user_id]], data)
        if not updated:
            for k, v in old_data.items():
                setattr(user, k, v)
            return False
        return True

    @staticmethod
    def to_record(user: User) -> typing.Dict:
        return {
            'username': user.username,
            'type': user.type,
            'password': user.password,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
            'id': user.id,
        }

    @staticmethod
    def from_record(record: typing.Dict) -> User:
        return User(**record)


@provider(UserRepository)
@inject('db')
def provide_user_repository(db: DatabaseAdapter) -> UserRepository:
    table_adapter = db.table('users')
    return UserRepository(table_adapter)
