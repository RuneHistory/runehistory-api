from cmdbus import Command
from ioccontainer import inject

from runehistory_api.app.services.account import AccountService
from runehistory_api.app.services.highscore import HighScoreService


class GetAccountCountCommand(Command):
    @inject('account_service')
    def __init__(self, account_service: AccountService = None):
        self.account_service = account_service

    def handle(self):
        return self.account_service.count()


class GetHighScoreCountCommand(Command):
    @inject('highscore_service')
    def __init__(self, highscore_service: HighScoreService = None):
        self.highscore_service = highscore_service

    def handle(self):
        return self.highscore_service.count()
