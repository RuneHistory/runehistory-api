from runehistory_api.domain.models.highscore import Skill


def test_skill_creation():
    skill = Skill(50, 30, 123456)
    assert isinstance(skill.rank, int)
    assert skill.rank == 50
    assert isinstance(skill.level, int)
    assert skill.level == 30
    assert isinstance(skill.experience, int)
    assert skill.experience == 123456


def test_skill_types():
    skill = Skill('50', '30', '123456')
    assert isinstance(skill.rank, int)
    assert skill.rank == 50
    assert isinstance(skill.level, int)
    assert skill.level == 30
    assert isinstance(skill.experience, int)
    assert skill.experience == 123456


def test_skill_encodable():
    skill = Skill(50, 30, 123456)
    assert skill.get_encodable() == {
        'rank': 50,
        'level': 30,
        'experience': 123456
    }
