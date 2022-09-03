try:
    import ujson as json
except ImportError:
    import json

from typing import Optional, Union

from ..object import Dictionaryable, JsonDeserializable, JsonSerializable, LoginUrl


class KeyboardButtonPollType(Dictionaryable):
    def __init__(self, type=''):
        self.type: str = type

    def to_dict(self):
        return {'type': self.type}


class KeyboardButton(Dictionaryable, JsonSerializable):
    def __init__(self, text: str, request_contact: Optional[bool] = None,
                 request_location: Optional[bool] = None, request_poll: Optional[KeyboardButtonPollType] = None):
        self.text: str = text
        self.request_contact: bool = request_contact
        self.request_location: bool = request_location
        self.request_poll: KeyboardButtonPollType = request_poll

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        json_dict = {'text': self.text}
        if self.request_contact is not None:
            json_dict['request_contact'] = self.request_contact
        if self.request_location is not None:
            json_dict['request_location'] = self.request_location
        if self.request_poll is not None:
            json_dict['request_poll'] = self.request_poll.to_dict()
        return json_dict


class InlineKeyboardButton(Dictionaryable, JsonSerializable, JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string)
        if 'login_url' in obj:
            obj['login_url'] = LoginUrl.de_json(obj.get('login_url'))
        return cls(**obj)

    def __init__(self, text, url=None, callback_data=None, switch_inline_query=None,
                 switch_inline_query_current_chat=None, callback_game=None, pay=None, login_url=None, **kwargs):
        self.text: str = text
        self.url: str = url
        self.callback_data: str = callback_data
        self.switch_inline_query: str = switch_inline_query
        self.switch_inline_query_current_chat: str = switch_inline_query_current_chat
        self.callback_game = callback_game  # Not Implemented
        self.pay: bool = pay
        self.login_url: LoginUrl = login_url

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        json_dict = {'text': self.text}
        if self.url:
            json_dict['url'] = self.url
        if self.callback_data:
            json_dict['callback_data'] = self.callback_data
        if self.switch_inline_query is not None:
            json_dict['switch_inline_query'] = self.switch_inline_query
        if self.switch_inline_query_current_chat is not None:
            json_dict['switch_inline_query_current_chat'] = self.switch_inline_query_current_chat
        if self.callback_game is not None:
            json_dict['callback_game'] = self.callback_game
        if self.pay is not None:
            json_dict['pay'] = self.pay
        if self.login_url is not None:
            json_dict['login_url'] = self.login_url.to_dict()
        return json_dict
