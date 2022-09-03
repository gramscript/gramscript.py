try:
    import ujson as json
except ImportError:
    import json
from ..object import Dictionaryable, JsonDeserializable, JsonSerializable


class User(JsonDeserializable, Dictionaryable, JsonSerializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string, dict_copy=False)
        return cls(**obj)

    def __init__(self, id, is_bot, first_name, last_name=None, username=None, language_code=None,
                 can_join_groups=None, can_read_all_group_messages=None, supports_inline_queries=None, **kwargs):
        self.id: int = id
        self.is_bot: bool = is_bot
        self.first_name: str = first_name
        self.username: str = username
        self.last_name: str = last_name
        self.language_code: str = language_code
        self.can_join_groups: bool = can_join_groups
        self.can_read_all_group_messages: bool = can_read_all_group_messages
        self.supports_inline_queries: bool = supports_inline_queries

    @property
    def full_name(self):
        full_name = self.first_name
        if self.last_name:
            full_name += ' {0}'.format(self.last_name)
        return full_name

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {'id': self.id,
                'is_bot': self.is_bot,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'username': self.username,
                'language_code': self.language_code,
                'can_join_groups': self.can_join_groups,
                'can_read_all_group_messages': self.can_read_all_group_messages,
                'supports_inline_queries': self.supports_inline_queries}
