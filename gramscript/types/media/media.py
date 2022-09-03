try:
    import ujson as json
except ImportError:
    import json
from typing import List

from ..object import Dictionaryable, JsonDeserializable, JsonSerializable


class Dice(JsonSerializable, Dictionaryable, JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string, dict_copy=False)
        return cls(**obj)

    def __init__(self, value, emoji, **kwargs):
        self.value: int = value
        self.emoji: str = emoji

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {'value': self.value,
                'emoji': self.emoji}


class PhotoSize(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string, dict_copy=False)
        return cls(**obj)

    def __init__(self, file_id, file_unique_id, width, height, file_size=None, **kwargs):
        self.file_id: str = file_id
        self.file_unique_id: str = file_unique_id
        self.width: int = width
        self.height: int = height
        self.file_size: int = file_size


class Audio(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string)
        if 'thumb' in obj and 'file_id' in obj['thumb']:
            obj['thumb'] = PhotoSize.de_json(obj['thumb'])
        else:
            obj['thumb'] = None
        return cls(**obj)

    def __init__(self, file_id, file_unique_id, duration, performer=None, title=None, file_name=None, mime_type=None,
                 file_size=None, thumb=None, **kwargs):
        self.file_id: str = file_id
        self.file_unique_id: str = file_unique_id
        self.duration: int = duration
        self.performer: str = performer
        self.title: str = title
        self.file_name: str = file_name
        self.mime_type: str = mime_type
        self.file_size: int = file_size
        self.thumb: PhotoSize = thumb


class Voice(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string, dict_copy=False)
        return cls(**obj)

    def __init__(self, file_id, file_unique_id, duration, mime_type=None, file_size=None, **kwargs):
        self.file_id: str = file_id
        self.file_unique_id: str = file_unique_id
        self.duration: int = duration
        self.mime_type: str = mime_type
        self.file_size: int = file_size


class Document(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string)
        if 'thumb' in obj and 'file_id' in obj['thumb']:
            obj['thumb'] = PhotoSize.de_json(obj['thumb'])
        else:
            obj['thumb'] = None
        return cls(**obj)

    def __init__(self, file_id, file_unique_id, thumb=None, file_name=None, mime_type=None, file_size=None, **kwargs):
        self.file_id: str = file_id
        self.file_unique_id: str = file_unique_id
        self.thumb: PhotoSize = thumb
        self.file_name: str = file_name
        self.mime_type: str = mime_type
        self.file_size: int = file_size


class Video(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string)
        if 'thumb' in obj and 'file_id' in obj['thumb']:
            obj['thumb'] = PhotoSize.de_json(obj['thumb'])
        return cls(**obj)

    def __init__(self, file_id, file_unique_id, width, height, duration, thumb=None, file_name=None, mime_type=None, file_size=None, **kwargs):
        self.file_id: str = file_id
        self.file_unique_id: str = file_unique_id
        self.width: int = width
        self.height: int = height
        self.duration: int = duration
        self.thumb: PhotoSize = thumb
        self.file_name: str = file_name
        self.mime_type: str = mime_type
        self.file_size: int = file_size


class VideoNote(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string)
        if 'thumb' in obj and 'file_id' in obj['thumb']:
            obj['thumb'] = PhotoSize.de_json(obj['thumb'])
        return cls(**obj)

    def __init__(self, file_id, file_unique_id, length, duration, thumb=None, file_size=None, **kwargs):
        self.file_id: str = file_id
        self.file_unique_id: str = file_unique_id
        self.length: int = length
        self.duration: int = duration
        self.thumb: PhotoSize = thumb
        self.file_size: int = file_size


class Contact(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string, dict_copy=False)
        return cls(**obj)

    def __init__(self, phone_number, first_name, last_name=None, user_id=None, vcard=None, **kwargs):
        self.phone_number: str = phone_number
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.user_id: int = user_id
        self.vcard: str = vcard


class Location(JsonDeserializable, JsonSerializable, Dictionaryable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string, dict_copy=False)
        return cls(**obj)

    def __init__(self, longitude, latitude, horizontal_accuracy=None,
                 live_period=None, heading=None, proximity_alert_radius=None, **kwargs):
        self.longitude: float = longitude
        self.latitude: float = latitude
        self.horizontal_accuracy: float = horizontal_accuracy
        self.live_period: int = live_period
        self.heading: int = heading
        self.proximity_alert_radius: int = proximity_alert_radius

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            "longitude": self.longitude,
            "latitude": self.latitude,
            "horizontal_accuracy": self.horizontal_accuracy,
            "live_period": self.live_period,
            "heading": self.heading,
            "proximity_alert_radius": self.proximity_alert_radius,
        }


class Venue(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string)
        obj['location'] = Location.de_json(obj['location'])
        return cls(**obj)

    def __init__(self, location, title, address, foursquare_id=None, foursquare_type=None,
                 google_place_id=None, google_place_type=None, **kwargs):
        self.location: Location = location
        self.title: str = title
        self.address: str = address
        self.foursquare_id: str = foursquare_id
        self.foursquare_type: str = foursquare_type
        self.google_place_id: str = google_place_id
        self.google_place_type: str = google_place_type


class UserProfilePhotos(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string)
        if 'photos' in obj:
            photos = [[PhotoSize.de_json(y) for y in x] for x in obj['photos']]
            obj['photos'] = photos
        return cls(**obj)

    def __init__(self, total_count, photos=None, **kwargs):
        self.total_count: int = total_count
        self.photos: List[PhotoSize] = photos


class File(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string, dict_copy=False)
        return cls(**obj)

    def __init__(self, file_id, file_unique_id, file_size, file_path, **kwargs):
        self.file_id: str = file_id
        self.file_unique_id: str = file_unique_id
        self.file_size: int = file_size
        self.file_path: str = file_path


class InputMedia(Dictionaryable, JsonSerializable):
    def __init__(self, type, media, caption=None, parse_mode=None, caption_entities=None):
        self.type: str = type
        self.media: str = media
        self.caption: Optional[str] = caption
        self.parse_mode: Optional[str] = parse_mode
        self.caption_entities: Optional[List[MessageEntity]] = caption_entities

        if is_string(self.media):
            self._media_name = ''
            self._media_dic = self.media
        else:
            self._media_name = generate_random_token()
            self._media_dic = 'attach://{0}'.format(self._media_name)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        json_dict = {'type': self.type, 'media': self._media_dic}
        if self.caption:
            json_dict['caption'] = self.caption
        if self.parse_mode:
            json_dict['parse_mode'] = self.parse_mode
        if self.caption_entities:
            json_dict['caption_entities'] = MessageEntity.to_list_of_dicts(
                self.caption_entities)
        return json_dict

    def convert_input_media(self):
        if is_string(self.media):
            return self.to_json(), None

        return self.to_json(), {self._media_name: self.media}


class InputMediaPhoto(InputMedia):
    def __init__(self, media, caption=None, parse_mode=None):
        if is_pil_image(media):
            media = pil_image_to_file(media)

        super(InputMediaPhoto, self).__init__(type="photo",
                                              media=media, caption=caption, parse_mode=parse_mode)

    def to_dict(self):
        return super(InputMediaPhoto, self).to_dict()


class InputMediaVideo(InputMedia):
    def __init__(self, media, thumb=None, caption=None, parse_mode=None, width=None, height=None, duration=None,
                 supports_streaming=None):
        super(InputMediaVideo, self).__init__(type="video",
                                              media=media, caption=caption, parse_mode=parse_mode)
        self.thumb = thumb
        self.width = width
        self.height = height
        self.duration = duration
        self.supports_streaming = supports_streaming

    def to_dict(self):
        ret = super(InputMediaVideo, self).to_dict()
        if self.thumb:
            ret['thumb'] = self.thumb
        if self.width:
            ret['width'] = self.width
        if self.height:
            ret['height'] = self.height
        if self.duration:
            ret['duration'] = self.duration
        if self.supports_streaming:
            ret['supports_streaming'] = self.supports_streaming
        return ret


class InputMediaAnimation(InputMedia):
    def __init__(self, media, thumb=None, caption=None, parse_mode=None, width=None, height=None, duration=None):
        super(InputMediaAnimation, self).__init__(type="animation",
                                                  media=media, caption=caption, parse_mode=parse_mode)
        self.thumb = thumb
        self.width = width
        self.height = height
        self.duration = duration

    def to_dict(self):
        ret = super(InputMediaAnimation, self).to_dict()
        if self.thumb:
            ret['thumb'] = self.thumb
        if self.width:
            ret['width'] = self.width
        if self.height:
            ret['height'] = self.height
        if self.duration:
            ret['duration'] = self.duration
        return ret


class InputMediaAudio(InputMedia):
    def __init__(self, media, thumb=None, caption=None, parse_mode=None, duration=None, performer=None, title=None):
        super(InputMediaAudio, self).__init__(type="audio",
                                              media=media, caption=caption, parse_mode=parse_mode)
        self.thumb = thumb
        self.duration = duration
        self.performer = performer
        self.title = title

    def to_dict(self):
        ret = super(InputMediaAudio, self).to_dict()
        if self.thumb:
            ret['thumb'] = self.thumb
        if self.duration:
            ret['duration'] = self.duration
        if self.performer:
            ret['performer'] = self.performer
        if self.title:
            ret['title'] = self.title
        return ret


class InputMediaDocument(InputMedia):
    def __init__(self, media, thumb=None, caption=None, parse_mode=None, disable_content_type_detection=None):
        super(InputMediaDocument, self).__init__(type="document",
                                                 media=media, caption=caption, parse_mode=parse_mode)
        self.thumb = thumb
        self.disable_content_type_detection = disable_content_type_detection

    def to_dict(self):
        ret = super(InputMediaDocument, self).to_dict()
        if self.thumb:
            ret['thumb'] = self.thumb
        if self.disable_content_type_detection is not None:
            ret['disable_content_type_detection'] = self.disable_content_type_detection
        return ret
