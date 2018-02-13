import typing
from datetime import datetime

from runehistory.app.database import TableAdapter
from runehistory.domain.models.account import Account


class AccountRepository:
    identifier = 'slug'

    def __init__(self, accounts: TableAdapter):
        self.accounts = accounts
        self.accounts.identifier = type(self).identifier

    def create(self, account: Account) -> Account:
        if account.created_at is None:
            account.created_at = datetime.utcnow()
        self.accounts.insert(AccountRepository.to_record(account))
        return account

    def find_one(self, slug: str) \
            -> typing.Union[Account, None]:
        record = self.accounts.find_one(slug)
        if record is None:
            return None
        return AccountRepository.from_record(record)

    def find(self, where: typing.List = None, fields: typing.List = None,
             limit: int = 100, offset: int = None,
             order: typing.List = None
             ) -> typing.List:
        results = self.accounts.find(where, fields, limit, offset, order)
        return [account for account in
                map(AccountRepository.from_record, results)]

    @staticmethod
    def to_record(account: Account) -> typing.Dict:
        return {
            'slug': account.slug,
            'nickname': account.nickname,
            'runs_unchanged': account.runs_unchanged,
            'last_run_at': account.last_run_at,
            'run_changed_at': account.run_changed_at,
            'created_at': account.created_at,
            'updated_at': account.updated_at,
        }

    @staticmethod
    def from_record(record: typing.Dict) -> Account:
        return Account(**record)
