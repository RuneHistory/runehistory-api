import typing

from runehistory.domain.models.account import Account

if typing.TYPE_CHECKING:
    from runehistory.app.repositories.account import AccountRepository


class AccountService:
    def __init__(self, account_repository: 'AccountRepository'):
        self.account_repository = account_repository

    def create(self, nickname: str) -> Account:
        account = Account(nickname)

        return self.account_repository.create(account)

    def find_one(self, slug: str) -> typing.Union[Account, None]:
        return self.account_repository.find_one(slug)

    def find(self, where: typing.Dict = None, fields: typing.List = None,
             limit: int = 100, offset: int = None,
             order: typing.List = None
             ) -> typing.List:
        return self.account_repository.find(where, fields, limit, offset,
                                            order)
