import typing
from datetime import datetime

from ioccontainer import provider, inject

from runehistory_api.domain.models.account import Account
from runehistory_api.domain.models.highscore import HighScore, Skill
from runehistory_api.app.repositories.highscore import HighScoreRepository


class HighScoreService:
    def __init__(self, highscore_repository: HighScoreRepository):
        self.highscore_repository = highscore_repository

    def create(self, account: Account, skills: typing.Dict) -> HighScore:
        skills = {name: Skill(**skill_dict) for name, skill_dict in
                  skills.items()}
        highscore = HighScore(account.id, **skills)
        return self.highscore_repository.create(highscore)

    def find_one_by_account(self, account_id: str,
                            id: str) -> typing.Union[HighScore, None]:
        return self.find_one([
            ['account_id', account_id],
            ['id', id],
        ])

    def find_one(self, where: typing.List = None, fields: typing.List = None) \
            -> typing.Union[HighScore, None]:
        return self.highscore_repository.find_one(where, fields)

    def find(self, created_after: datetime = None,
             created_before: datetime = None,
             skills: typing.List = None) -> typing.List:
        where = []
        order = []
        fields = None
        if created_after:
            where.append(['created_at', '>=', created_after])
        if created_before:
            where.append(['created_at', '<', created_before])
        order.append(['created_at', 'desc'])
        if skills:
            fields = ['id', 'experience_hash', 'account_id', 'created_at',
                      'updated_at']
            for skill in skills:
                fields.append('skills.{}'.format(skill))
        return self.highscore_repository.find(
            where, fields=fields, order=order
        )

    def find_by_xp_sum(self, account_id: str, xp_sum: int) -> typing.List:
        return self.highscore_repository.find(
            [
                ['account_id', account_id],
                ['xp_sum', xp_sum],
            ],
            limit=2
        )


@provider(HighScoreService)
@inject('repo')
def provide_highscore_service(
        repo: HighScoreRepository) -> HighScoreService:
    return HighScoreService(repo)
