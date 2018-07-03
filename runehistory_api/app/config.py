import yaml


class Config:
    def __init__(self, path: str):
        self.path = path
        self.cfg = {}
        self.parse()

    def parse(self):
        with open(self.path, 'r') as f:
            self.cfg = yaml.load(f)

    @property
    def secret(self) -> str:
        return self.cfg.get('secret')

    @property
    def db_connection_string(self) -> str:
        return self.cfg.get('db_connection_string')

    @property
    def db_host(self) -> str:
        return self.cfg.get('db_host', '127.0.0.1')

    @property
    def db_port(self) -> int:
        return self.cfg.get('db_port', 27017)
