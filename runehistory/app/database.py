import typing


class DatabaseAdapter:
    def table(self, table: str) -> 'TableAdapter': pass


class TableAdapter:
    def __init__(self, id: str = None, ids: typing.List = None):
        self.id = id
        self.ids = ids

    def insert(self, data: typing.Any) -> typing.Dict: pass

    def find_one(self, where: typing.List = None, fields: typing.List = None
                 ) -> typing.Union[typing.Dict, None]: pass

    def find(self, where: typing.List = None, fields: typing.List = None,
             limit: int = 100, offset: int = None,
             order: typing.List = None
             ) -> typing.List: pass

    def update_one(self, where: typing.List, data: typing.Dict) -> bool: pass
