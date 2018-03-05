import typing
from datetime import datetime

import dateutil.parser
from cmdbus import Command
from evntbus import evntbus
from ioccontainer import inject

from runehistory_api.app.exceptions import RHError, NotFoundError
from runehistory_api.app.services.account import AccountService
from runehistory_api.app.services.highscore import HighScoreService
from runehistory_api.app.events.highscore import HighScoreCreatedEvent, \
    GotHighScoreEvent, GotHighScoresEvent


class CreateHighScoreCommand(Command):
    @inject('account_service', 'highscore_service')
    def __init__(self, slug: str,
                 skills: typing.Dict,
                 account_service: AccountService = None,
                 highscore_service: HighScoreService = None):
        self.slug = slug
        self.skills = skills
        self.account_service = account_service
        self.highscore_service = highscore_service

    def handle(self):
        account = self.account_service.find_one_by_slug(self.slug)
        if not account:
            raise NotFoundError('Account not found: {}'.format(self.slug))
        highscore = self.highscore_service.create(account, self.skills)
        evntbus.emit(HighScoreCreatedEvent(account, highscore))
        existing = self.highscore_service.find_by_xp_sum(
            account.id, highscore.calc_xp_sum()
        )
        now = datetime.utcnow()
        new_data = {
            'runs_unchanged': account.runs_unchanged + 1,
            'last_run_at': now,
        }
        if len(existing) == 1:
            new_data['run_changed_at'] = now
            new_data['runs_unchanged'] = 0
        updated = self.account_service.update_one([
            ['id', account.id]
        ], new_data)

        if not updated:
            raise RHError('Failed to update account')

        return highscore


class GetHighScoreCommand(Command):
    @inject('account_service', 'highscore_service')
    def __init__(self, slug: str, id: str,
                 account_service: AccountService = None,
                 highscore_service: HighScoreService = None):
        self.slug = slug
        self.id = id
        self.account_service = account_service
        self.highscore_service = highscore_service

    def handle(self):
        account = self.account_service.find_one_by_slug(self.slug)
        if not account:
            raise NotFoundError('Account not found: {}'.format(self.slug))
        highscore = self.highscore_service.find_one_by_account(
            account.id, self.id
        )
        if not highscore:
            raise NotFoundError('Highscore not found: {}'.format(self.id))
        evntbus.emit(GotHighScoreEvent(account, highscore))
        return highscore


class GetHighScoresCommand(Command):
    @inject('account_service', 'highscore_service')
    def __init__(self, slug: str,
                 created_after: datetime = None,
                 created_before: datetime = None,
                 skills: typing.List = None,
                 account_service: AccountService = None,
                 highscore_service: HighScoreService = None):
        if isinstance(created_after, str):
            created_after = dateutil.parser.parse(created_after)
        if isinstance(created_before, str):
            created_before = dateutil.parser.parse(created_before)
        self.slug = slug
        self.created_after = created_after
        self.created_before = created_before
        self.skills = skills
        self.account_service = account_service
        self.highscore_service = highscore_service

    def handle(self):
        account = self.account_service.find_one_by_slug(self.slug)
        if not account:
            raise NotFoundError('Account not found: {}'.format(self.slug))
        highscores = self.highscore_service.find(
            self.created_after, self.created_before, self.skills
        )
        evntbus.emit(GotHighScoresEvent(account, highscores))
        return highscores
