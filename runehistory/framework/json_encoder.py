from flask.json import JSONEncoder
from datetime import datetime


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            to_json = getattr(obj, 'get_encodable', None)
            if callable(to_json):
                return obj.get_encodable()
            if isinstance(obj, datetime):
                if obj.utcoffset() is not None:
                    obj = obj - obj.utcoffset()
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
