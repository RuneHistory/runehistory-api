import typing
from datetime import datetime

import dateutil.parser
from cmdbus import Command
from evntbus import evntbus

from runehistory.app.exceptions import NotFoundError
from runehistory.app.services.account import AccountService
from runehistory.app.services.highscore import HighScoreService
from runehistory.app.events.highscore import HighScoreCreatedEvent, \
    GotHighScoreEvent, GotHighScoresEvent


class CreateHighScoreCommand(Command):
    def __init__(self, account_service: AccountService,
                 highscore_service: HighScoreService, slug: str,
                 skills: typing.Dict):
        self.account_service = account_service
        self.highscore_service = highscore_service
        self.slug = slug
        self.skills = skills

    def handle(self):
        account = self.account_service.find_one_by_slug(self.slug)
        if not account:
            raise NotFoundError('Account not found: {}'.format(self.slug))
        highscore = self.highscore_service.create(account, self.skills)
        evntbus.emit(HighScoreCreatedEvent(highscore))
        return highscore


class GetHighScoreCommand(Command):
    def __init__(self, account_service: AccountService,
                 highscore_service: HighScoreService, slug: str, id: str):
        self.account_service = account_service
        self.highscore_service = highscore_service
        self.slug = slug
        self.id = id

    def handle(self):
        account = self.account_service.find_one_by_slug(self.slug)
        if not account:
            raise NotFoundError('Account not found: {}'.format(self.slug))
        highscore = self.highscore_service.find_one_by_account(
            account.id, self.id
        )
        if not highscore:
            raise NotFoundError('Highscore not found: {}'.format(self.id))
        evntbus.emit(GotHighScoreEvent(highscore))
        return highscore


class GetHighScoresCommand(Command):
    def __init__(self, account_service: AccountService,
                 highscore_service: HighScoreService, slug: str,
                 created_after: datetime = None,
                 created_before: datetime = None,
                 skills: typing.List = None):
        if isinstance(created_after, str):
            created_after = dateutil.parser.parse(created_after)
        if isinstance(created_before, str):
            created_before = dateutil.parser.parse(created_before)
        self.account_service = account_service
        self.highscore_service = highscore_service
        self.slug = slug
        self.created_after = created_after
        self.created_before = created_before
        self.skills = skills

    def handle(self):
        account = self.account_service.find_one_by_slug(self.slug)
        if not account:
            raise NotFoundError('Account not found: {}'.format(self.slug))
        highscores = self.highscore_service.find(
            self.created_after, self.created_before, self.skills
        )
        evntbus.emit(GotHighScoresEvent(highscores))
        return highscores
