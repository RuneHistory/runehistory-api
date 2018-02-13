import typing
from datetime import datetime

from runehistory.domain.models.account import Account

if typing.TYPE_CHECKING:
    from runehistory.app.repositories.account import AccountRepository


class AccountService:
    def __init__(self, account_repository: 'AccountRepository'):
        self.account_repository = account_repository

    def create(self, nickname: str) -> Account:
        account = Account(nickname)

        return self.account_repository.create(account)

    def find_one_by_slug(self, slug: str) -> typing.Union[Account, None]:
        return self.find_one([['slug', slug]])

    def find_one(self, where: typing.List = None, fields: typing.List = None)\
            -> typing.Union[Account, None]:
        return self.account_repository.find_one(where, fields)

    def find(self, last_ran_before: datetime = None,
             runs_unchanged_min: int = None, runs_unchanged_max: int = None,
             prioritise: bool = False) -> typing.List:
        where = []
        order = []
        if last_ran_before:
            where.append({'or': [
                ['last_ran_before', '<', last_ran_before],
                ['last_ran_before', '=', None],
            ]})
        if runs_unchanged_min:
            where.append(['runs_unchanged', '>=', runs_unchanged_min])
        if runs_unchanged_max:
            where.append(['runs_unchanged', '<=', runs_unchanged_max])
        if prioritise:
            order.append(['runs_unchanged', 'asc'])
            order.append(['last_run_at', 'asc'])

        where = where if len(where) else None
        order = order if len(order) else None
        return self.account_repository.find(where, order=order)
