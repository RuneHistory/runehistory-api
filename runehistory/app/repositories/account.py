import typing

from runehistory.app.database import TableAdapter
from runehistory.domain.models.account import Account


class AccountRepository:
    identifier = 'slug'

    def __init__(self, accounts: TableAdapter):
        self.accounts = accounts
        self.accounts.identifier = type(self).identifier

    def create(self, account: Account) -> Account:
        self.accounts.insert(AccountRepository.to_record(account))
        return account

    def find(self, slug: str) \
            -> typing.Union[Account, None]:
        record = self.accounts.find(slug)
        if record is None:
            return None
        return AccountRepository.from_record(record)

    @staticmethod
    def to_record(account: Account) -> typing.Dict:
        return {
            'slug': account.slug,
            'nickname': account.nickname,
            'runs_unchanged': account.runs_unchanged,
            'last_run_at': account.last_run_at,
            'run_changed_at': account.run_changed_at,
        }

    @staticmethod
    def from_record(record: typing.Dict) -> Account:
        return Account(**record)
