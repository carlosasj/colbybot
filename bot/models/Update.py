import json
from . import Message
from functools import lru_cache


class Update:
    def __init__(self, body):
        data = json.loads(body.decode("utf-8"))
        self.json = data
        print(data)
        self.update_id = data['update_id']
        self.is_edited = 'edited_message' in 'data'
        if 'message' in data:
            self.message = Message(data['message'])

    @property
    @lru_cache()
    def is_valid_request(self):
        return hasattr(self, 'message')
