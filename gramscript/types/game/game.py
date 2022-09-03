from typing import List

from ..chat_and_user.user import User
from ..media.media import PhotoSize
from ..message.message import MessageEntity
from ..object import JsonDeserializable


class Game(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if (json_string is None):
            return None
        obj = cls.check_json(json_string)
        obj['photo'] = Game.parse_photo(obj['photo'])
        if 'text_entities' in obj:
            obj['text_entities'] = Game.parse_entities(obj['text_entities'])
        if 'animation' in obj:
            obj['animation'] = Animation.de_json(obj['animation'])
        return cls(**obj)

    @classmethod
    def parse_photo(cls, photo_size_array):
        return [PhotoSize.de_json(ps) for ps in photo_size_array]

    @classmethod
    def parse_entities(cls, message_entity_array):
        return [MessageEntity.de_json(me) for me in message_entity_array]

    def __init__(self, title, description, photo, text=None, text_entities=None, animation=None, **kwargs):
        self.title: str = title
        self.description: str = description
        self.photo: List[PhotoSize] = photo
        self.text: str = text
        self.text_entities: List[MessageEntity] = text_entities
        self.animation: Animation = animation


class Animation(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if (json_string is None):
            return None
        obj = cls.check_json(json_string)
        if 'thumb' in obj and 'file_id' in obj['thumb']:
            obj["thumb"] = PhotoSize.de_json(obj['thumb'])
        else:
            obj['thumb'] = None
        return cls(**obj)

    def __init__(self, file_id, file_unique_id, width=None, height=None, duration=None,
                 thumb=None, file_name=None, mime_type=None, file_size=None, **kwargs):
        self.file_id: str = file_id
        self.file_unique_id: str = file_unique_id
        self.width: int = width
        self.height: int = height
        self.duration: int = duration
        self.thumb: PhotoSize = thumb
        self.file_name: str = file_name
        self.mime_type: str = mime_type
        self.file_size: int = file_size


class GameHighScore(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if (json_string is None):
            return None
        obj = cls.check_json(json_string)
        obj['user'] = User.de_json(obj['user'])
        return cls(**obj)

    def __init__(self, position, user, score, **kwargs):
        self.position: int = position
        self.user: User = user
        self.score: int = score
