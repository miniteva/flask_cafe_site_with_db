import json
from typing import Any, Optional, Dict
from redis import Redis, ConnectionError, DataError


class RedisCache:

    def __init__(self, config):
        self.config = config
        self.conn = self._connect()

    def _connect(self):
        conn = Redis(**self.config)
        return conn

    def _update_connect_if_need(self):
        try:
            self.conn.ping()
        except ConnectionError:
            self.conn = self._connect()

    def set_value(self, name, value, ttl=0):
        self._update_connect_if_need()
        try:
            value1 = json.dumps(value)
            self.conn.set(name=name, value=value1)
            if ttl > 0:     # Время жизни словаря
                self.conn.expire(name, ttl)
            return True
        except DataError as e:
            print(f"error while setting key-value: {str(e)}")
            return False

    def get_value(self, name):
        self._update_connect_if_need()
        value = self.conn.get(name)
        if value:
            return json.loads(value)
        return None
