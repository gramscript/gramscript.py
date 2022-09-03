try:
    import ujson as json
except ImportError:
    import json

from typing import List
from gramscript.types.chat_and_user.user import User

from gramscript.types.message import Message
from gramscript.types.message.message import MessageEntity
from gramscript.types.object import Dictionaryable, JsonDeserializable, JsonSerializable


class PollOption(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if (json_string is None):
            return None
        obj = cls.check_json(json_string, dict_copy=False)
        return cls(**obj)

    def __init__(self, text, voter_count=0, **kwargs):
        self.text: str = text
        self.voter_count: int = voter_count
    # Converted in _convert_poll_options
    # def to_json(self):
    #     # send_poll Option is a simple string: https://core.telegram.org/bots/api#sendpoll
    #     return json.dumps(self.text)


class Poll(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string)
        obj['poll_id'] = obj.pop('id')
        options = [PollOption.de_json(opt) for opt in obj['options']]
        obj['options'] = options or None
        if 'explanation_entities' in obj:
            obj['explanation_entities'] = Message.parse_entities(
                obj['explanation_entities'])

        return cls(**obj)

    def __init__(
            self,
            question, options,
            poll_id=None, total_voter_count=None, is_closed=None, is_anonymous=None, poll_type=None,
            allows_multiple_answers=None, correct_option_id=None, explanation=None, explanation_entities=None,
            open_period=None, close_date=None, **kwargs):
        self.id: str = poll_id
        self.question: str = question
        self.options: List[PollOption] = options
        self.total_voter_count: int = total_voter_count
        self.is_closed: bool = is_closed
        self.is_anonymous: bool = is_anonymous
        self.type: str = poll_type
        self.allows_multiple_answers: bool = allows_multiple_answers
        self.correct_option_id: int = correct_option_id
        self.explanation: str = explanation
        # Default state of entities is None. if (explanation_entities is not None) else []
        self.explanation_entities: List[MessageEntity] = explanation_entities
        self.open_period: int = open_period
        self.close_date: int = close_date

    def add(self, option):
        if type(option) is PollOption:
            self.options.append(option)
        else:
            self.options.append(PollOption(option))


class PollAnswer(JsonSerializable, JsonDeserializable, Dictionaryable):
    @classmethod
    def de_json(cls, json_string):
        if (json_string is None):
            return None
        obj = cls.check_json(json_string)
        obj['user'] = User.de_json(obj['user'])
        return cls(**obj)

    def __init__(self, poll_id, user, option_ids, **kwargs):
        self.poll_id: str = poll_id
        self.user: User = user
        self.option_ids: List[int] = option_ids

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {'poll_id': self.poll_id,
                'user': self.user.to_dict(),
                'option_ids': self.option_ids}
