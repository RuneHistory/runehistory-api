import typing

from runehistory.domain.models.account import Account
from runehistory.domain.models.highscore import HighScore, Skill

if typing.TYPE_CHECKING:
    from runehistory.app.repositories.highscore import HighScoreRepository


class HighScoreService:
    def __init__(self, highscore_repository: 'HighScoreRepository'):
        self.highscore_repository = highscore_repository

    def create(self, account: Account, skills: typing.Dict) -> HighScore:
        skills = {name: Skill(**skill_dict) for name, skill_dict in skills.items()}
        highscore = HighScore(account.id, **skills)
        return self.highscore_repository.create(highscore)

    def find_one_by_account(self, account_id: str,
                            id: str)-> typing.Union[HighScore, None]:
        return self.find_one([
            ['account_id', account_id],
            ['id', id],
        ])

    def find_one(self, where: typing.List = None, fields: typing.List = None)\
            -> typing.Union[HighScore, None]:
        return self.highscore_repository.find_one(where, fields)

    def find(self) -> typing.List:
        return self.highscore_repository.find()
