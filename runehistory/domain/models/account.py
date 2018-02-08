from datetime import datetime

from slugify import slugify


class Account:
    def __init__(self, nickname: str, slug: str = None,
                 runs_unchanged: int = 0, last_run_at: datetime = None,
                 run_changed_at: datetime = None):
        self.nickname = nickname
        if slug is None:
            slug = slugify(nickname)
        self.slug = slug
        self.runs_unchanged = runs_unchanged
        self.last_run_at = last_run_at
        self.run_changed_at = run_changed_at
