from datetime import datetime

from slugify import slugify


class Account:
    def __init__(self, nickname: str, slug: str = None,
                 runs_unchanged: int = 0, last_run_at: datetime = None,
                 run_changed_at: datetime = None, created_at: datetime = None,
                 updated_at: datetime = None, id: str = None):
        self.nickname = nickname
        if slug is None:
            slug = slugify(nickname)
        self.slug = slug
        self.runs_unchanged = runs_unchanged
        self.last_run_at = last_run_at
        self.run_changed_at = run_changed_at
        self.created_at = created_at
        self.updated_at = updated_at
        self.id = id

    def get_encodable(self):
        return {
            'nickname': self.nickname,
            'slug': self.slug,
            'runs_unchanged': self.runs_unchanged,
            'last_run_at': self.last_run_at.isoformat() \
                if self.last_run_at else None,
            'run_changed_at': self.run_changed_at,
            'created_at': self.created_at.isoformat() \
                if self.created_at else None,
            'updated_at': self.updated_at.isoformat() \
                if self.updated_at else None,
            'id': self.id,
        }
