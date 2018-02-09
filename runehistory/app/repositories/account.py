import typing

from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from runehistory.app.exceptions import DuplicateError
from runehistory.domain.models.account import Account


class AccountRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create(self, account: Account) -> Account:
        try:
            self.collection.insert_one(AccountRepository.to_record(account))
        except DuplicateKeyError:
            raise DuplicateError('Account already exists')
        return account

    def get(self, slug: str) -> typing.Union[Account, None]:
        record = self.collection.find_one({'_id': slug})
        if record is None:
            return None
        return AccountRepository.from_record(record)

    @staticmethod
    def to_record(account: Account) -> typing.Dict:
        return {
            '_id': account.slug,
            'nickname': account.nickname,
            'runs_unchanged': account.runs_unchanged,
            'last_run_at': account.last_run_at,
            'run_changed_at': account.run_changed_at,
        }

    @staticmethod
    def from_record(record: typing.Dict) -> Account:
        return Account(record['nickname'], record['_id'],
                       record['runs_unchanged'], record['last_run_at'],
                       record['run_changed_at'])
