try:
    import ujson as json
except ImportError:
    import json
from typing import List

from ..media import PhotoSize
from ..object import Dictionaryable, JsonDeserializable, JsonSerializable


class StickerSet(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if (json_string is None):
            return None
        obj = cls.check_json(json_string)
        stickers = [Sticker.de_json(s) for s in obj['stickers']]
        obj['stickers'] = stickers
        if 'thumb' in obj and 'file_id' in obj['thumb']:
            obj['thumb'] = PhotoSize.de_json(obj['thumb'])
        else:
            obj['thumb'] = None
        return cls(**obj)

    def __init__(self, name, title, is_animated, contains_masks, stickers, thumb=None, **kwargs):
        self.name: str = name
        self.title: str = title
        self.is_animated: bool = is_animated
        self.contains_masks: bool = contains_masks
        self.stickers: List[Sticker] = stickers
        self.thumb: PhotoSize = thumb


class Sticker(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if (json_string is None):
            return None
        obj = cls.check_json(json_string)
        if 'thumb' in obj and 'file_id' in obj['thumb']:
            obj['thumb'] = PhotoSize.de_json(obj['thumb'])
        else:
            obj['thumb'] = None
        if 'mask_position' in obj:
            obj['mask_position'] = MaskPosition.de_json(obj['mask_position'])
        return cls(**obj)

    def __init__(self, file_id, file_unique_id, width, height, is_animated,
                 thumb=None, emoji=None, set_name=None, mask_position=None, file_size=None, **kwargs):
        self.file_id: str = file_id
        self.file_unique_id: str = file_unique_id
        self.width: int = width
        self.height: int = height
        self.is_animated: bool = is_animated
        self.thumb: PhotoSize = thumb
        self.emoji: str = emoji
        self.set_name: str = set_name
        self.mask_position: MaskPosition = mask_position
        self.file_size: int = file_size


class MaskPosition(Dictionaryable, JsonDeserializable, JsonSerializable):
    @classmethod
    def de_json(cls, json_string):
        if (json_string is None):
            return None
        obj = cls.check_json(json_string, dict_copy=False)
        return cls(**obj)

    def __init__(self, point, x_shift, y_shift, scale, **kwargs):
        self.point: str = point
        self.x_shift: float = x_shift
        self.y_shift: float = y_shift
        self.scale: float = scale

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {'point': self.point, 'x_shift': self.x_shift, 'y_shift': self.y_shift, 'scale': self.scale}
