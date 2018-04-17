from datetime import datetime


class User:
    def __init__(self, username: str, password: str, type: str,
                 created_at: datetime = None, updated_at: datetime = None,
                 id: str = None):
        self.username = username
        self.password = password
        self.type = type
        self.created_at = created_at
        self.updated_at = updated_at
        self.id = id

    def get_encodable(self):
        return {
            'username': self.username,
            'type': self.type,
            'created_at': self.created_at.isoformat()
            if self.created_at else None,
            'updated_at': self.updated_at.isoformat()
            if self.updated_at else None,
            'id': self.id,
        }
