import typing


class DatabaseAdapter:
    def table(self, table: str) -> 'TableAdapter': pass


class TableAdapter:
    def __init__(self, identifier: str = None):
        self.identifier = identifier

    def insert(self, data: typing.Any) -> typing.Dict: pass

    def find(self, identifier: typing.Any,
             fields: typing.List = None
             ) -> typing.Union[typing.Dict, None]: pass
