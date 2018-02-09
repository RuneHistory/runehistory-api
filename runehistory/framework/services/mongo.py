import typing

from pymongo.errors import DuplicateKeyError

from runehistory.app.database import DatabaseAdapter, TableAdapter
from runehistory.app.exceptions import DuplicateError

if typing.TYPE_CHECKING:
    from pymongo.database import Database
    from pymongo.collection import Collection


class MongoDatabaseAdapter(DatabaseAdapter):
    def __init__(self, db: 'Database'):
        self.db = db

    def table(self, table: str, identifier: str = None) -> 'MongoTableAdapter':
        return MongoTableAdapter(self.db[table], identifier)


class MongoTableAdapter(TableAdapter):
    def __init__(self, collection: 'Collection', identifier: str = None):
        super().__init__(identifier)
        self.collection = collection

    def _record_to_id(self, record: typing.Dict) -> typing.Dict:
        if self.identifier is not None:
            record['_id'] = record.pop(self.identifier)
        return record

    def _record_from_id(self, record: typing.Dict) -> typing.Dict:
        if self.identifier is not None:
            record[self.identifier] = record.pop('_id')
        return record

    def _projection_from_list(self, fields: typing.List = None) -> typing.Dict:
        if not fields:
            return {}
        fields = ['_id' if field is self.identifier else field for field in
                  tuple(fields)]
        projection = {field: 1 for field in fields}
        if '_id' not in fields:
            projection['_id'] = 0
        return projection

    def insert(self, record: typing.Dict) -> typing.Dict:
        try:
            record = self._record_to_id(record)
            self.collection.insert_one(record)
        except DuplicateKeyError:
            raise DuplicateError('Duplicate record')
        return self._record_from_id(record)

    def find(self, identifier: typing.Any,
             fields: typing.List = None) -> typing.Union[typing.Dict, None]:
        record = self.collection.find_one({'_id': identifier},
                                          projection=fields)
        if record is None:
            return None
        return self._record_from_id(record)
