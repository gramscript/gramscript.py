from gramscript.types.chat_and_user.user import User
from gramscript.types.message.message import Message
from gramscript.types.object import JsonDeserializable


class CallbackQuery(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string)
        if "data" not in obj:
            # "data" field is Optional in the API, but historically is mandatory in the class constructor
            obj['data'] = None
        obj['from_user'] = User.de_json(obj.pop('from'))
        if 'message' in obj:
            obj['message'] = Message.de_json(obj.get('message'))
        return cls(**obj)

    def __init__(self, id, from_user, data, chat_instance, message=None, inline_message_id=None, game_short_name=None, **kwargs):
        self.id: int = id
        self.from_user: User = from_user
        self.message: Message = message
        self.inline_message_id: str = inline_message_id
        self.chat_instance: str = chat_instance
        self.data: str = data
        self.game_short_name: str = game_short_name
