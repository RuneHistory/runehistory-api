from evntbus import Event


class AccountEvent(Event):
    def __init__(self, account):
        self.account = account


class AccountCreatedEvent(AccountEvent):
    pass


class AccountUpdatedEvent(AccountEvent):
    pass
