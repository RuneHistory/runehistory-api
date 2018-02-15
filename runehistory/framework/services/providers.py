from pymongo import MongoClient
from ioccontainer import inject, provider, scopes

from runehistory.app.database import DatabaseAdapter
from runehistory.framework.services.mongo import MongoDatabaseAdapter
from runehistory.app.repositories.account import AccountRepository
from runehistory.framework.services.account import AccountService
from runehistory.app.repositories.highscore import HighScoreRepository
from runehistory.framework.services.highscore import HighScoreService


def register_service_providers():
    @provider(MongoClient, scopes.SINGLETON)
    def provide_mongo() -> MongoClient:
        return MongoClient('127.0.0.1', 27017)

    @provider(MongoDatabaseAdapter, scopes.SINGLETON)
    @inject('client')
    def provide_mongo_adapter(client: MongoClient) -> MongoDatabaseAdapter:
        return MongoDatabaseAdapter(client.test)

    @provider(DatabaseAdapter)
    @inject('adapter')
    def provide_db(adapter: MongoDatabaseAdapter) -> DatabaseAdapter:
        return adapter

    @provider(AccountRepository)
    @inject('db')
    def provide_account_repository(db: DatabaseAdapter) -> AccountRepository:
        table_adapter = db.table('accounts')
        return AccountRepository(table_adapter)

    @provider(AccountService)
    @inject('repo')
    def provide_account_service(repo: AccountRepository) -> AccountService:
        return AccountService(repo)

    @provider(HighScoreRepository)
    @inject('db')
    def provide_highscore_repository(
            db: DatabaseAdapter) -> HighScoreRepository:
        table_adapter = db.table('highscores')
        return HighScoreRepository(table_adapter)

    @provider(HighScoreService)
    @inject('repo')
    def provide_highscore_service(
            repo: HighScoreRepository) -> HighScoreService:
        return HighScoreService(repo)
