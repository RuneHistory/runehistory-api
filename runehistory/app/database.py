import typing


class DatabaseAdapter:
    def table(self, table: str) -> 'TableAdapter': pass


class TableAdapter:
    def __init__(self, identifier: str = None):
        self.identifier = identifier

    def insert(self, data: typing.Any) -> typing.Dict: pass

    def find_one(self, identifier: typing.Any,
                 fields: typing.List = None
                 ) -> typing.Union[typing.Dict, None]: pass

    def find(self, where: typing.List = None, fields: typing.List = None,
             limit: int = 100, offset: int = None,
             order: typing.List = None
             ) -> typing.List: pass
