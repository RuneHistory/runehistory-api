from pymongo import MongoClient

from ioccontainer import inject, provider, scopes
from runehistory.framework.services.account import AccountService
from runehistory.app.repositories.account import AccountRepository


def register_service_providers():
    @provider(MongoClient, scopes.SINGLETON)
    def provide_db():
        return MongoClient('127.0.0.1', 27017).test

    @provider(AccountRepository)
    @inject('db')
    def provide_account_repository(db: MongoClient):
        return AccountRepository(db.accounts)

    @provider(AccountService)
    @inject('repo')
    def provide_account_service(repo: AccountRepository):
        return AccountService(repo)
