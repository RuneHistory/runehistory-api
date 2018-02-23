import typing
from datetime import datetime

from ioccontainer import provider, inject

from runehistory.app.database import DatabaseAdapter, TableAdapter
from runehistory.domain.models.account import Account


class AccountRepository:
    id = 'id'
    ids = []

    def __init__(self, accounts: TableAdapter):
        self.accounts = accounts
        self.accounts.id = type(self).id
        self.accounts.ids = type(self).ids

    def create(self, account: Account) -> Account:
        if account.created_at is None:
            account.created_at = datetime.utcnow()
        record = self.accounts.insert(AccountRepository.to_record(account))
        return AccountRepository.from_record(record)

    def find_one(self, where: typing.List = None, fields: typing.List = None) \
            -> typing.Union[Account, None]:
        record = self.accounts.find_one(where, fields)
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

    def update_one(self, where: typing.List, data: typing.Dict) -> bool:
        return self.accounts.update_one(where, data)

    def update(self, account: Account, data: typing.Dict) -> bool:
        account_id = getattr(account, type(self).id, None)
        if not account_id:
            return False
        if 'nickname' in data:
            data['slug'] = account.generate_slug(data['nickname'])
        data['updated_at'] = datetime.utcnow()
        old_data = dict()
        for k, v in data.items():
            old_data[k] = getattr(account, k)
            setattr(account, k, v)
        updated = self.update_one([[type(self).id, account_id]], data)
        if not updated:
            for k, v in old_data.items():
                setattr(account, k, v)
            return False
        return True

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
            'id': account.id,
        }

    @staticmethod
    def from_record(record: typing.Dict) -> Account:
        return Account(**record)


@provider(AccountRepository)
@inject('db')
def provide_account_repository(db: DatabaseAdapter) -> AccountRepository:
    table_adapter = db.table('accounts')
    return AccountRepository(table_adapter)
