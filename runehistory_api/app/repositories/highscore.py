import typing
from datetime import datetime

from ioccontainer import provider, inject

from runehistory_api.app.database import DatabaseAdapter, TableAdapter
from runehistory_api.domain.models.highscore import HighScore, Skill


class HighScoreRepository:
    id = 'id'
    ids = ['account_id']

    def __init__(self, highscores: TableAdapter):
        self.highscores = highscores
        self.highscores.id = type(self).id
        self.highscores.ids = type(self).ids

    def create(self, highscore: HighScore) -> HighScore:
        if highscore.created_at is None:
            highscore.created_at = datetime.utcnow()
        record = self.highscores.insert(type(self).to_record(highscore))
        return type(self).from_record(record)

    def find_one(self, where: typing.List = None, fields: typing.List = None,
                 offset: int = None, order: typing.List = None
                 ) -> typing.Union[HighScore, None]:
        record = self.highscores.find_one(where, fields, offset, order)
        if record is None:
            return None
        return type(self).from_record(record)

    def find(self, where: typing.List = None, fields: typing.List = None,
             limit: int = None, offset: int = None,
             order: typing.List = None
             ) -> typing.List:
        results = self.highscores.find(where, fields, limit, offset, order)
        return [highscore for highscore in
                map(type(self).from_record, results)]

    def count(self) -> int:
        return self.highscores.count()

    @staticmethod
    def to_record(highscore: HighScore) -> typing.Dict:
        return {
            'account_id': highscore.account_id,
            'id': highscore.id,
            'created_at': highscore.created_at,
            'skills': {
                name: {'rank': int(skill.rank), 'level': int(skill.level),
                       'experience': int(skill.experience)} if skill else None
                for name, skill in highscore.skills.items()
            },
            'xp_sum': highscore.calc_xp_sum()
        }

    @staticmethod
    def from_record(record: typing.Dict) -> HighScore:
        skills = {name: Skill(**skill_dict) for name, skill_dict in
                  record.pop('skills').items()}
        if 'xp_sum' in record:
            record.pop('xp_sum')
        record.update(skills)
        return HighScore(**record)


@provider(HighScoreRepository)
@inject('db')
def provide_highscore_repository(
        db: DatabaseAdapter) -> HighScoreRepository:
    table_adapter = db.table('highscores')
    return HighScoreRepository(table_adapter)
