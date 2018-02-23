from datetime import datetime

SKILLS = ['overall', 'attack', 'defence', 'strength', 'hitpoints',
          'ranged', 'prayer', 'magic', 'cooking', 'woodcutting',
          'fletching', 'fishing', 'firemaking', 'crafting', 'smithing',
          'mining', 'herblore', 'agility', 'theiving', 'slayer',
          'farming', 'hunter']


class Skill:
    def __init__(self, rank: int, level: int, experience: int):
        self.rank = rank
        self.level = level
        self.experience = experience

    def get_encodable(self):
        return {
            'rank': self.rank,
            'level': self.level,
            'experience': self.experience,
        }


class HighScore:
    def __init__(self, account_id: str, id: str = None,
                 created_at: datetime = None,
                 **kwargs: Skill):
        self.account_id = account_id
        self.id = id
        self.created_at = created_at
        self._skills = dict()
        for name, skill in kwargs.items():
            if name not in SKILLS:
                raise AttributeError('{key} is not a valid skill'.format(
                    key=name
                ))
            setattr(self, name, skill)

    @property
    def skills(self):
        return {skill: getattr(self, skill) for skill in SKILLS}

    def __setattr__(self, key: str, value):
        if key in SKILLS:
            if not isinstance(value, Skill):
                raise AttributeError('A skill must be an instance of {}'
                                     .format(Skill.__name__))
            self._skills[key] = value
        super().__setattr__(key, value)

    def __getattr__(self, item: str):
        if item in SKILLS:
            if item not in self._skills:
                return None
            return self._skills[item]
        return super().__getattribute__(item)

    def get_encodable(self):
        skills = {name: skill for name, skill in self.skills.items() if
                  skill is not None}
        return {
            'account_id': self.account_id,
            'id': self.id,
            'created_at': self.created_at.isoformat() \
                if self.created_at else None,
            'skills': skills,
        }
