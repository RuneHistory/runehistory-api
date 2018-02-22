import typing

from cmdbus import Command
from evntbus import evntbus

from runehistory.app.exceptions import NotFoundError
from runehistory.app.services.account import AccountService
from runehistory.app.services.highscore import HighScoreService
from runehistory.app.events.highscore import HighScoreCreatedEvent


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
        return highscore
