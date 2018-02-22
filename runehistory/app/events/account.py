from evntbus import Event


class AccountEvent(Event):
    def __init__(self, account):
        self.account = account


class AccountCreatedEvent(AccountEvent):
    pass


class AccountUpdatedEvent(AccountEvent):
    pass


class GotAccountEvent(AccountEvent):
    pass


class GotAccountsEvent(Event):
    def __init__(self, accounts):
        self.accounts = accounts
