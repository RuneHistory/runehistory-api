import typing

from pymongo.errors import DuplicateKeyError
from pymongo import ASCENDING, DESCENDING, MongoClient
from bson import ObjectId
from bson.errors import InvalidId
from ioccontainer import provider, inject, scopes

from runehistory_api.app.database import DatabaseAdapter, TableAdapter
from runehistory_api.app.exceptions import DuplicateError, AdapterError

if typing.TYPE_CHECKING:
    from pymongo.database import Database
    from pymongo.collection import Collection


class MongoDatabaseAdapter(DatabaseAdapter):
    def __init__(self, db: 'Database'):
        self.db = db

    def table(self, table: str, id: str = None,
              ids: typing.List = None) -> 'MongoTableAdapter':
        if ids is None:
            ids = []
        return MongoTableAdapter(self.db[table], id, ids)


class MongoTableAdapter(TableAdapter):
    def __init__(self, collection: 'Collection', id: str = None,
                 ids: typing.List = None):
        super().__init__(id, ids)
        self.collection = collection

    def _record_to_id(self, record: typing.Dict) -> typing.Dict:
        return {self._key_to_id(key): self._value_to_id(key, value)
                for key, value in record.items()}

    def _record_from_id(self, record: typing.Dict) -> typing.Dict:
        return {self._key_from_id(key): self._value_from_id(value)
                for key, value in record.items()}

    def _key_to_id(self, key: str):
        if key == self.id:
            return '_id'
        return key

    def _value_to_id(self, key: str, value: typing.Any):
        try:
            if key == self.id or key in self.ids and isinstance(value, str):
                return ObjectId(value)
        except InvalidId:
            raise ValueError('Invalid id: {}'.format(value))
        return value

    def _key_from_id(self, key: str):
        if key == '_id':
            return self.id
        return key

    def _value_from_id(self, value: typing.Any):
        if isinstance(value, ObjectId):
            return str(value)
        return value

    def _key_value_to_id(
            self, key: str, value: str
    ) -> (str, typing.Any):
        return self._key_to_id(key), self._value_to_id(key, value)

    def _key_value_from_id(
            self, key: str, value: str
    ) -> (str, typing.Any):
        return self._key_from_id(key), self._value_from_id(value)

    def _projection_from_list(self, fields: typing.List = None) -> typing.Dict:
        if not fields:
            return {}
        fields = [self._key_to_id(field) for field in
                  tuple(fields)]
        projection = {field: 1 for field in fields}
        if '_id' not in fields:
            projection['_id'] = 0
        return projection

    def insert(self, record: typing.Dict) -> typing.Dict:
        try:
            record = self._record_to_id(record)
            if record['_id'] is None:
                record.pop('_id')
            self.collection.insert_one(record)
        except DuplicateKeyError:
            raise DuplicateError('Duplicate record')
        return self._record_from_id(record)

    def find_one(self, where: typing.List = None, fields: typing.List = None) \
            -> typing.Union[typing.Dict, None]:
        parsed_where = self._parse_conditions(where)
        record = self.collection.find_one(
            parsed_where,
            projection=fields
        )
        if record is None:
            return None
        return self._record_from_id(record)

    def find(self, where: typing.List = None, fields: typing.List = None,
             limit: int = 100, offset: int = None,
             order: typing.List = None
             ) -> typing.List:
        parsed_where = self._parse_conditions(where)

        results = self.collection.find(parsed_where, fields).limit(limit)
        if offset is not None:
            results = results.skip(offset)
        if order is not None:
            updated_order = []
            for item in order:
                direction = DESCENDING if item[1] is 'desc' else ASCENDING
                updated_order.append((item[0], direction))
            results = results.sort(updated_order)
        return [self._record_from_id(record) for record in results]

    def update_one(self, where: typing.List, data: typing.Dict) -> bool:
        parsed_where = self._parse_conditions(where)
        parsed_data = {'$set': data}
        results = self.collection.update_one(parsed_where, parsed_data)
        return results.modified_count > 0

    def _parse_conditions(self, conditions: typing.Union[typing.List, None],
                          statement: str = 'and') -> typing.Dict:
        if not conditions:
            return dict()
        parsed_conditions = dict()
        parsed_conditions['${}'.format(statement)] = [
            self._parse_condition(condition) for condition in conditions]

        return parsed_conditions

    def _parse_condition(
            self, condition: typing.Union[typing.List, typing.Dict]) \
            -> typing.Dict:
        if isinstance(condition, list):
            return self._parse_condition_list(condition)
        if isinstance(condition, dict):
            return self._parse_condition_dict(condition)

    def _parse_condition_list(self, condition: typing.List) -> typing.Dict:
        if len(condition) is 2:
            key, value = self._key_value_to_id(condition[0], condition[1])
            if isinstance(value, dict):
                return self._parse_condition_dict(value)
            return {key: {'$eq': value}}
        if len(condition) is 3:
            key, value = self._key_value_to_id(condition[0], condition[2])
            operator = condition[1]
            if operator == '=':
                return {key: {'$eq': value}}
            if operator == '>':
                return {key: {'$gt': value}}
            if operator == '>=':
                return {key: {'$gte': value}}
            if operator == '<':
                return {key: {'$lt': value}}
            if operator == '<=':
                return {key: {'$lte': value}}
        raise AdapterError('Unhandled condition')

    def _parse_condition_dict(self, conditions: typing.Dict) -> typing.Dict:
        parsed_conditions = {}
        for statement, sub_conditions in conditions.items():
            parsed_conditions.update(
                self._parse_conditions(sub_conditions, statement))
        return parsed_conditions


@provider(MongoClient, scopes.SINGLETON)
def provide_mongo() -> MongoClient:
    return MongoClient('127.0.0.1', 27017)


@provider(MongoDatabaseAdapter, scopes.SINGLETON)
@inject('client')
def provide_mongo_adapter(client: MongoClient) -> MongoDatabaseAdapter:
    return MongoDatabaseAdapter(client.test)
