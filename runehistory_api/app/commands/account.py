import typing
from datetime import datetime

import dateutil.parser
from cmdbus import Command
from evntbus import evntbus
from ioccontainer import inject

from runehistory_api.app.exceptions import NotFoundError, RHError
from runehistory_api.app.services.account import AccountService
from runehistory_api.app.events.account import AccountCreatedEvent,\
    AccountUpdatedEvent, GotAccountEvent, GotAccountsEvent


class CreateAccountCommand(Command):
    @inject('account_service')
    def __init__(self, nickname: str, account_service: AccountService = None):
        self.nickname = nickname
        self.account_service = account_service

    def handle(self):
        account = self.account_service.create(self.nickname)
        evntbus.emit(AccountCreatedEvent(account))
        return account


class GetAccountsCommand(Command):
    @inject('account_service')
    def __init__(self, last_ran_before: datetime = None,
                 runs_unchanged_min: int = None,
                 runs_unchanged_max: int = None,
                 prioritise: bool = False,
                 account_service: AccountService = None):
        if isinstance(last_ran_before, str):
            last_ran_before = dateutil.parser.parse(last_ran_before)
        self.last_ran_before = last_ran_before
        self.runs_unchanged_min = runs_unchanged_min
        self.runs_unchanged_max = runs_unchanged_max
        self.prioritise = prioritise
        self.account_service = account_service

    def handle(self):
        accounts = self.account_service.find(
            self.last_ran_before, self.runs_unchanged_min,
            self.runs_unchanged_max, self.prioritise
        )
        evntbus.emit(GotAccountsEvent(accounts))
        return accounts


class UpdateAccountCommand(Command):
    @inject('account_service')
    def __init__(self, slug: str,
                 data: typing.Dict,
                 account_service: AccountService = None):
        self.slug = slug
        self.data = data
        self.account_service = account_service

    def handle(self):
        account = self.account_service.find_one_by_slug(self.slug)
        if not account:
            raise NotFoundError('Account not found: {}'.format(self.slug))
        update_data = dict()
        valid_updates = ['nickname']
        for update in valid_updates:
            if update not in self.data:
                continue
            update_data[update] = self.data[update]

        if not len(update_data):
            raise ValueError('No updates specified')

        updated = self.account_service.update(account, update_data)
        if not updated:
            raise RHError('Unable to update account')
        evntbus.emit(AccountUpdatedEvent(account))
        return account


class GetAccountCommand(Command):
    @inject('account_service')
    def __init__(self, slug: str, account_service: AccountService = None):
        self.slug = slug
        self.account_service = account_service

    def handle(self):
        account = self.account_service.find_one_by_slug(self.slug)
        if not account:
            raise NotFoundError('Account not found: {}'.format(self.slug))
        evntbus.emit(GotAccountEvent(account))
        return account
