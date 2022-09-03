from abc import ABC
from typing import List, Optional
from gramscript.types.chat_and_user.user import User
from gramscript.types.media.media import Location
from gramscript.types.message.message import MessageEntity

from gramscript.types.object import Dictionaryable, JsonDeserializable, JsonSerializable
from gramscript.types.payment.payment import LabeledPrice

try:
    import ujson as json
except ImportError:
    import json


class InlineQuery(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string)
        obj['from_user'] = User.de_json(obj.pop('from'))
        if 'location' in obj:
            obj['location'] = Location.de_json(obj['location'])
        return cls(**obj)

    def __init__(self, id, from_user, query, offset, chat_type=None, location=None, **kwargs):
        """
        This object represents an incoming inline query.
        When the user sends an empty query, your bot could
        return some default or trending results.
        :param id: string Unique identifier for this query
        :param from_user: User Sender
        :param query: String Text of the query
        :param chat_type: String Type of the chat, from which the inline query was sent. 
            Can be either “sender” for a private chat with the inline query sender, 
            “private”, “group”, “supergroup”, or “channel”. 
        :param offset: String Offset of the results to be returned, can be controlled by the bot
        :param location: Sender location, only for bots that request user location
        :return: InlineQuery Object
        """
        self.id: int = id
        self.from_user: User = from_user
        self.query: str = query
        self.offset: str = offset
        self.chat_type: str = chat_type
        self.location: Location = location


class InputTextMessageContent(Dictionaryable):
    def __init__(self, message_text, parse_mode=None, entities=None, disable_web_page_preview=None):
        self.message_text: str = message_text
        self.parse_mode: str = parse_mode
        self.entities: List[MessageEntity] = entities
        self.disable_web_page_preview: bool = disable_web_page_preview

    def to_dict(self):
        json_dict = {'message_text': self.message_text}
        if self.parse_mode:
            json_dict['parse_mode'] = self.parse_mode
        if self.entities:
            json_dict['entities'] = MessageEntity.to_list_of_dicts(
                self.entities)
        if self.disable_web_page_preview is not None:
            json_dict['disable_web_page_preview'] = self.disable_web_page_preview
        return json_dict


class InputLocationMessageContent(Dictionaryable):
    def __init__(self, latitude, longitude, horizontal_accuracy=None, live_period=None, heading=None, proximity_alert_radius=None):
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.horizontal_accuracy: float = horizontal_accuracy
        self.live_period: int = live_period
        self.heading: int = heading
        self.proximity_alert_radius: int = proximity_alert_radius

    def to_dict(self):
        json_dict = {'latitude': self.latitude, 'longitude': self.longitude}
        if self.horizontal_accuracy:
            json_dict['horizontal_accuracy'] = self.horizontal_accuracy
        if self.live_period:
            json_dict['live_period'] = self.live_period
        if self.heading:
            json_dict['heading'] = self.heading
        if self.proximity_alert_radius:
            json_dict['proximity_alert_radius'] = self.proximity_alert_radius
        return json_dict


class InputVenueMessageContent(Dictionaryable):
    def __init__(self, latitude, longitude, title, address, foursquare_id=None, foursquare_type=None,
                 google_place_id=None, google_place_type=None):
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.title: str = title
        self.address: str = address
        self.foursquare_id: str = foursquare_id
        self.foursquare_type: str = foursquare_type
        self.google_place_id: str = google_place_id
        self.google_place_type: str = google_place_type

    def to_dict(self):
        json_dict = {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'title': self.title,
            'address': self.address
        }
        if self.foursquare_id:
            json_dict['foursquare_id'] = self.foursquare_id
        if self.foursquare_type:
            json_dict['foursquare_type'] = self.foursquare_type
        if self.google_place_id:
            json_dict['google_place_id'] = self.google_place_id
        if self.google_place_type:
            json_dict['google_place_type'] = self.google_place_type
        return json_dict


class InputContactMessageContent(Dictionaryable):
    def __init__(self, phone_number, first_name, last_name=None, vcard=None):
        self.phone_number: str = phone_number
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.vcard: str = vcard

    def to_dict(self):
        json_dict = {'phone_number': self.phone_number,
                     'first_name': self.first_name}
        if self.last_name:
            json_dict['last_name'] = self.last_name
        if self.vcard:
            json_dict['vcard'] = self.vcard
        return json_dict


class InputInvoiceMessageContent(Dictionaryable):
    def __init__(self, title, description, payload, provider_token, currency, prices,
                 max_tip_amount=None, suggested_tip_amounts=None, provider_data=None,
                 photo_url=None, photo_size=None, photo_width=None, photo_height=None,
                 need_name=None, need_phone_number=None, need_email=None, need_shipping_address=None,
                 send_phone_number_to_provider=None, send_email_to_provider=None,
                 is_flexible=None):
        self.title: str = title
        self.description: str = description
        self.payload: str = payload
        self.provider_token: str = provider_token
        self.currency: str = currency
        self.prices: List[LabeledPrice] = prices
        self.max_tip_amount: Optional[int] = max_tip_amount
        self.suggested_tip_amounts: Optional[List[int]] = suggested_tip_amounts
        self.provider_data: Optional[str] = provider_data
        self.photo_url: Optional[str] = photo_url
        self.photo_size: Optional[int] = photo_size
        self.photo_width: Optional[int] = photo_width
        self.photo_height: Optional[int] = photo_height
        self.need_name: Optional[bool] = need_name
        self.need_phone_number: Optional[bool] = need_phone_number
        self.need_email: Optional[bool] = need_email
        self.need_shipping_address: Optional[bool] = need_shipping_address
        self.send_phone_number_to_provider: Optional[bool] = send_phone_number_to_provider
        self.send_email_to_provider: Optional[bool] = send_email_to_provider
        self.is_flexible: Optional[bool] = is_flexible

    def to_dict(self):
        json_dict = {
            'title': self.title,
            'description': self.description,
            'payload': self.payload,
            'provider_token': self.provider_token,
            'currency': self.currency,
            'prices': [LabeledPrice.to_dict(lp) for lp in self.prices]
        }
        if self.max_tip_amount:
            json_dict['max_tip_amount'] = self.max_tip_amount
        if self.suggested_tip_amounts:
            json_dict['suggested_tip_amounts'] = self.suggested_tip_amounts
        if self.provider_data:
            json_dict['provider_data'] = self.provider_data
        if self.photo_url:
            json_dict['photo_url'] = self.photo_url
        if self.photo_size:
            json_dict['photo_size'] = self.photo_size
        if self.photo_width:
            json_dict['photo_width'] = self.photo_width
        if self.photo_height:
            json_dict['photo_height'] = self.photo_height
        if self.need_name is not None:
            json_dict['need_name'] = self.need_name
        if self.need_phone_number is not None:
            json_dict['need_phone_number'] = self.need_phone_number
        if self.need_email is not None:
            json_dict['need_email'] = self.need_email
        if self.need_shipping_address is not None:
            json_dict['need_shipping_address'] = self.need_shipping_address
        if self.send_phone_number_to_provider is not None:
            json_dict['send_phone_number_to_provider'] = self.send_phone_number_to_provider
        if self.send_email_to_provider is not None:
            json_dict['send_email_to_provider'] = self.send_email_to_provider
        if self.is_flexible is not None:
            json_dict['is_flexible'] = self.is_flexible
        return json_dict


class ChosenInlineResult(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string)
        obj['from_user'] = User.de_json(obj.pop('from'))
        if 'location' in obj:
            obj['location'] = Location.de_json(obj['location'])
        return cls(**obj)

    def __init__(self, result_id, from_user, query, location=None, inline_message_id=None, **kwargs):
        """
        This object represents a result of an inline query
        that was chosen by the user and sent to their chat partner.
        :param result_id: string The unique identifier for the result that was chosen.
        :param from_user: User The user that chose the result.
        :param query: String The query that was used to obtain the result.
        :return: ChosenInlineResult Object.
        """
        self.result_id: str = result_id
        self.from_user: User = from_user
        self.location: Location = location
        self.inline_message_id: str = inline_message_id
        self.query: str = query


class InlineQueryResultBase(ABC, Dictionaryable, JsonSerializable):
    # noinspection PyShadowingBuiltins
    def __init__(self, type, id, title=None, caption=None, input_message_content=None,
                 reply_markup=None, caption_entities=None, parse_mode=None):
        self.type = type
        self.id = id
        self.title = title
        self.caption = caption
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup
        self.caption_entities = caption_entities
        self.parse_mode = parse_mode

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        json_dict = {
            'type': self.type,
            'id': self.id
        }
        if self.title:
            json_dict['title'] = self.title
        if self.caption:
            json_dict['caption'] = self.caption
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dict()
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dict()
        if self.caption_entities:
            json_dict['caption_entities'] = MessageEntity.to_list_of_dicts(
                self.caption_entities)
        if self.parse_mode:
            json_dict['parse_mode'] = self.parse_mode
        return json_dict


class InlineQueryResultArticle(InlineQueryResultBase):
    def __init__(self, id, title, input_message_content, reply_markup=None,
                 url=None, hide_url=None, description=None, thumb_url=None, thumb_width=None, thumb_height=None):
        """
        Represents a link to an article or web page.
        :param id: Unique identifier for this result, 1-64 Bytes.
        :param title: Title of the result.
        :param input_message_content: InputMessageContent : Content of the message to be sent
        :param reply_markup: InlineKeyboardMarkup : Inline keyboard attached to the message
        :param url: URL of the result.
        :param hide_url: Pass True, if you don't want the URL to be shown in the message.
        :param description: Short description of the result.
        :param thumb_url: Url of the thumbnail for the result.
        :param thumb_width: Thumbnail width.
        :param thumb_height: Thumbnail height
        :return:
        """
        super().__init__('article', id, title=title,
                         input_message_content=input_message_content, reply_markup=reply_markup)
        self.url = url
        self.hide_url = hide_url
        self.description = description
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    def to_dict(self):
        json_dict = super().to_dict()
        if self.url:
            json_dict['url'] = self.url
        if self.hide_url:
            json_dict['hide_url'] = self.hide_url
        if self.description:
            json_dict['description'] = self.description
        if self.thumb_url:
            json_dict['thumb_url'] = self.thumb_url
        if self.thumb_width:
            json_dict['thumb_width'] = self.thumb_width
        if self.thumb_height:
            json_dict['thumb_height'] = self.thumb_height
        return json_dict


class InlineQueryResultPhoto(InlineQueryResultBase):
    def __init__(self, id, photo_url, thumb_url, photo_width=None, photo_height=None, title=None,
                 description=None, caption=None, caption_entities=None, parse_mode=None, reply_markup=None, input_message_content=None):
        """
        Represents a link to a photo.
        :param id: Unique identifier for this result, 1-64 bytes
        :param photo_url: A valid URL of the photo. Photo must be in jpeg format. Photo size must not exceed 5MB
        :param thumb_url: URL of the thumbnail for the photo
        :param photo_width: Width of the photo.
        :param photo_height: Height of the photo.
        :param title: Title for the result.
        :param description: Short description of the result.
        :param caption: Caption of the photo to be sent, 0-200 characters.
        :param parse_mode: Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or
        inline URLs in the media caption.
        :param reply_markup: InlineKeyboardMarkup : Inline keyboard attached to the message
        :param input_message_content: InputMessageContent : Content of the message to be sent instead of the photo
        :return:
        """
        super().__init__('photo', id, title=title, caption=caption,
                         input_message_content=input_message_content, reply_markup=reply_markup,
                         parse_mode=parse_mode, caption_entities=caption_entities)
        self.photo_url = photo_url
        self.thumb_url = thumb_url
        self.photo_width = photo_width
        self.photo_height = photo_height
        self.description = description

    def to_dict(self):
        json_dict = super().to_dict()
        json_dict['photo_url'] = self.photo_url
        json_dict['thumb_url'] = self.thumb_url
        if self.photo_width:
            json_dict['photo_width'] = self.photo_width
        if self.photo_height:
            json_dict['photo_height'] = self.photo_height
        if self.description:
            json_dict['description'] = self.description
        return json_dict


class InlineQueryResultGif(InlineQueryResultBase):
    def __init__(self, id, gif_url, thumb_url, gif_width=None, gif_height=None,
                 title=None, caption=None, caption_entities=None,
                 reply_markup=None, input_message_content=None, gif_duration=None, parse_mode=None,
                 thumb_mime_type=None):
        """
        Represents a link to an animated GIF file.
        :param id: Unique identifier for this result, 1-64 bytes.
        :param gif_url: A valid URL for the GIF file. File size must not exceed 1MB
        :param thumb_url: URL of the static thumbnail (jpeg or gif) for the result.
        :param gif_width: Width of the GIF.
        :param gif_height: Height of the GIF.
        :param title: Title for the result.
        :param caption:  Caption of the GIF file to be sent, 0-200 characters
        :param reply_markup: InlineKeyboardMarkup : Inline keyboard attached to the message
        :param input_message_content: InputMessageContent : Content of the message to be sent instead of the photo
        :return:
        """
        super().__init__('gif', id, title=title, caption=caption,
                         input_message_content=input_message_content, reply_markup=reply_markup,
                         parse_mode=parse_mode, caption_entities=caption_entities)
        self.gif_url = gif_url
        self.gif_width = gif_width
        self.gif_height = gif_height
        self.thumb_url = thumb_url
        self.gif_duration = gif_duration
        self.thumb_mime_type = thumb_mime_type

    def to_dict(self):
        json_dict = super().to_dict()
        json_dict['gif_url'] = self.gif_url
        if self.gif_width:
            json_dict['gif_width'] = self.gif_width
        if self.gif_height:
            json_dict['gif_height'] = self.gif_height
        json_dict['thumb_url'] = self.thumb_url
        if self.gif_duration:
            json_dict['gif_duration'] = self.gif_duration
        if self.thumb_mime_type:
            json_dict['thumb_mime_type'] = self.thumb_mime_type
        return json_dict


class InlineQueryResultMpeg4Gif(InlineQueryResultBase):
    def __init__(self, id, mpeg4_url, thumb_url, mpeg4_width=None, mpeg4_height=None,
                 title=None, caption=None, caption_entities=None,
                 parse_mode=None, reply_markup=None, input_message_content=None, mpeg4_duration=None,
                 thumb_mime_type=None):
        """
        Represents a link to a video animation (H.264/MPEG-4 AVC video without sound).
        :param id: Unique identifier for this result, 1-64 bytes
        :param mpeg4_url: A valid URL for the MP4 file. File size must not exceed 1MB
        :param thumb_url: URL of the static thumbnail (jpeg or gif) for the result
        :param mpeg4_width: Video width
        :param mpeg4_height: Video height
        :param title: Title for the result
        :param caption: Caption of the MPEG-4 file to be sent, 0-200 characters
        :param parse_mode: Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text
        or inline URLs in the media caption.
        :param reply_markup: InlineKeyboardMarkup : Inline keyboard attached to the message
        :param input_message_content: InputMessageContent : Content of the message to be sent instead of the photo
        :return:
        """
        super().__init__('mpeg4_gif', id, title=title, caption=caption,
                         input_message_content=input_message_content, reply_markup=reply_markup,
                         parse_mode=parse_mode, caption_entities=caption_entities)
        self.mpeg4_url = mpeg4_url
        self.mpeg4_width = mpeg4_width
        self.mpeg4_height = mpeg4_height
        self.thumb_url = thumb_url
        self.mpeg4_duration = mpeg4_duration
        self.thumb_mime_type = thumb_mime_type

    def to_dict(self):
        json_dict = super().to_dict()
        json_dict['mpeg4_url'] = self.mpeg4_url
        if self.mpeg4_width:
            json_dict['mpeg4_width'] = self.mpeg4_width
        if self.mpeg4_height:
            json_dict['mpeg4_height'] = self.mpeg4_height
        json_dict['thumb_url'] = self.thumb_url
        if self.mpeg4_duration:
            json_dict['mpeg4_duration '] = self.mpeg4_duration
        if self.thumb_mime_type:
            json_dict['thumb_mime_type'] = self.thumb_mime_type
        return json_dict


class InlineQueryResultVideo(InlineQueryResultBase):
    def __init__(self, id, video_url, mime_type, thumb_url,
                 title, caption=None, caption_entities=None, parse_mode=None,
                 video_width=None, video_height=None, video_duration=None,
                 description=None, reply_markup=None, input_message_content=None):
        """
        Represents link to a page containing an embedded video player or a video file.
        :param id: Unique identifier for this result, 1-64 bytes
        :param video_url: A valid URL for the embedded video player or video file
        :param mime_type: Mime type of the content of video url, “text/html” or “video/mp4”
        :param thumb_url: URL of the thumbnail (jpeg only) for the video
        :param title: Title for the result
        :param parse_mode: Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or
        inline URLs in the media caption.
        :param video_width: Video width
        :param video_height: Video height
        :param video_duration: Video duration in seconds
        :param description: Short description of the result
        :return:
        """
        super().__init__('video', id, title=title, caption=caption,
                         input_message_content=input_message_content, reply_markup=reply_markup,
                         parse_mode=parse_mode, caption_entities=caption_entities)
        self.video_url = video_url
        self.mime_type = mime_type
        self.thumb_url = thumb_url
        self.video_width = video_width
        self.video_height = video_height
        self.video_duration = video_duration
        self.description = description

    def to_dict(self):
        json_dict = super().to_dict()
        json_dict['video_url'] = self.video_url
        json_dict['mime_type'] = self.mime_type
        json_dict['thumb_url'] = self.thumb_url
        if self.video_height:
            json_dict['video_height'] = self.video_height
        if self.video_duration:
            json_dict['video_duration'] = self.video_duration
        if self.description:
            json_dict['description'] = self.description
        return json_dict


class InlineQueryResultAudio(InlineQueryResultBase):
    def __init__(self, id, audio_url, title,
                 caption=None, caption_entities=None, parse_mode=None, performer=None,
                 audio_duration=None, reply_markup=None, input_message_content=None):
        super().__init__('audio', id, title=title, caption=caption,
                         input_message_content=input_message_content, reply_markup=reply_markup,
                         parse_mode=parse_mode, caption_entities=caption_entities)
        self.audio_url = audio_url
        self.performer = performer
        self.audio_duration = audio_duration

    def to_dict(self):
        json_dict = super().to_dict()
        json_dict['audio_url'] = self.audio_url
        if self.performer:
            json_dict['performer'] = self.performer
        if self.audio_duration:
            json_dict['audio_duration'] = self.audio_duration
        return json_dict


class InlineQueryResultVoice(InlineQueryResultBase):
    def __init__(self, id, voice_url, title, caption=None, caption_entities=None,
                 parse_mode=None, voice_duration=None, reply_markup=None, input_message_content=None):
        super().__init__('voice', id, title=title, caption=caption,
                         input_message_content=input_message_content, reply_markup=reply_markup,
                         parse_mode=parse_mode, caption_entities=caption_entities)
        self.voice_url = voice_url
        self.voice_duration = voice_duration

    def to_dict(self):
        json_dict = super().to_dict()
        json_dict['voice_url'] = self.voice_url
        if self.voice_duration:
            json_dict['voice_duration'] = self.voice_duration
        return json_dict


class InlineQueryResultDocument(InlineQueryResultBase):
    def __init__(self, id, title, document_url, mime_type, caption=None, caption_entities=None,
                 parse_mode=None, description=None, reply_markup=None, input_message_content=None,
                 thumb_url=None, thumb_width=None, thumb_height=None):
        super().__init__('document', id, title=title, caption=caption,
                         input_message_content=input_message_content, reply_markup=reply_markup,
                         parse_mode=parse_mode, caption_entities=caption_entities)
        self.document_url = document_url
        self.mime_type = mime_type
        self.description = description
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    def to_dict(self):
        json_dict = super().to_dict()
        json_dict['document_url'] = self.document_url
        json_dict['mime_type'] = self.mime_type
        if self.description:
            json_dict['description'] = self.description
        if self.thumb_url:
            json_dict['thumb_url'] = self.thumb_url
        if self.thumb_width:
            json_dict['thumb_width'] = self.thumb_width
        if self.thumb_height:
            json_dict['thumb_height'] = self.thumb_height
        return json_dict


class InlineQueryResultLocation(InlineQueryResultBase):
    def __init__(self, id, title, latitude, longitude, horizontal_accuracy, live_period=None, reply_markup=None,
                 input_message_content=None, thumb_url=None, thumb_width=None, thumb_height=None, heading=None, proximity_alert_radius=None):
        super().__init__('location', id, title=title,
                         input_message_content=input_message_content, reply_markup=reply_markup)
        self.latitude = latitude
        self.longitude = longitude
        self.horizontal_accuracy = horizontal_accuracy
        self.live_period = live_period
        self.heading: int = heading
        self.proximity_alert_radius: int = proximity_alert_radius
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    def to_dict(self):
        json_dict = super().to_dict()
        json_dict['latitude'] = self.latitude
        json_dict['longitude'] = self.longitude
        if self.horizontal_accuracy:
            json_dict['horizontal_accuracy'] = self.horizontal_accuracy
        if self.live_period:
            json_dict['live_period'] = self.live_period
        if self.heading:
            json_dict['heading'] = self.heading
        if self.proximity_alert_radius:
            json_dict['proximity_alert_radius'] = self.proximity_alert_radius
        if self.thumb_url:
            json_dict['thumb_url'] = self.thumb_url
        if self.thumb_width:
            json_dict['thumb_width'] = self.thumb_width
        if self.thumb_height:
            json_dict['thumb_height'] = self.thumb_height
        return json_dict


class InlineQueryResultVenue(InlineQueryResultBase):
    def __init__(self, id, title, latitude, longitude, address, foursquare_id=None, foursquare_type=None,
                 reply_markup=None, input_message_content=None, thumb_url=None,
                 thumb_width=None, thumb_height=None, google_place_id=None, google_place_type=None):
        super().__init__('venue', id, title=title,
                         input_message_content=input_message_content, reply_markup=reply_markup)
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.foursquare_id = foursquare_id
        self.foursquare_type = foursquare_type
        self.google_place_id = google_place_id
        self.google_place_type = google_place_type
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    def to_dict(self):
        json_dict = super().to_dict()
        json_dict['latitude'] = self.latitude
        json_dict['longitude'] = self.longitude
        json_dict['address'] = self.address
        if self.foursquare_id:
            json_dict['foursquare_id'] = self.foursquare_id
        if self.foursquare_type:
            json_dict['foursquare_type'] = self.foursquare_type
        if self.google_place_id:
            json_dict['google_place_id'] = self.google_place_id
        if self.google_place_type:
            json_dict['google_place_type'] = self.google_place_type
        if self.thumb_url:
            json_dict['thumb_url'] = self.thumb_url
        if self.thumb_width:
            json_dict['thumb_width'] = self.thumb_width
        if self.thumb_height:
            json_dict['thumb_height'] = self.thumb_height
        return json_dict


class InlineQueryResultContact(InlineQueryResultBase):
    def __init__(self, id, phone_number, first_name, last_name=None, vcard=None,
                 reply_markup=None, input_message_content=None,
                 thumb_url=None, thumb_width=None, thumb_height=None):
        super().__init__('contact', id,
                         input_message_content=input_message_content, reply_markup=reply_markup)
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.vcard = vcard
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    def to_dict(self):
        json_dict = super().to_dict()
        json_dict['phone_number'] = self.phone_number
        json_dict['first_name'] = self.first_name
        if self.last_name:
            json_dict['last_name'] = self.last_name
        if self.vcard:
            json_dict['vcard'] = self.vcard
        if self.thumb_url:
            json_dict['thumb_url'] = self.thumb_url
        if self.thumb_width:
            json_dict['thumb_width'] = self.thumb_width
        if self.thumb_height:
            json_dict['thumb_height'] = self.thumb_height
        return json_dict


class InlineQueryResultGame(InlineQueryResultBase):
    def __init__(self, id, game_short_name, reply_markup=None):
        super().__init__('game', id, reply_markup=reply_markup)
        self.game_short_name = game_short_name

    def to_dict(self):
        json_dict = super().to_dict()
        json_dict['game_short_name'] = self.game_short_name
        return json_dict


class InlineQueryResultCachedBase(ABC, JsonSerializable):
    def __init__(self):
        self.type = None
        self.id = None
        self.title = None
        self.description = None
        self.caption = None
        self.reply_markup = None
        self.input_message_content = None
        self.parse_mode = None
        self.caption_entities = None
        self.payload_dic = {}

    def to_json(self):
        json_dict = self.payload_dic
        json_dict['type'] = self.type
        json_dict['id'] = self.id
        if self.title:
            json_dict['title'] = self.title
        if self.description:
            json_dict['description'] = self.description
        if self.caption:
            json_dict['caption'] = self.caption
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dict()
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dict()
        if self.parse_mode:
            json_dict['parse_mode'] = self.parse_mode
        if self.caption_entities:
            json_dict['caption_entities'] = MessageEntity.to_list_of_dicts(
                self.caption_entities)
        return json.dumps(json_dict)


class InlineQueryResultCachedPhoto(InlineQueryResultCachedBase):
    def __init__(self, id, photo_file_id, title=None, description=None,
                 caption=None, caption_entities=None, parse_mode=None,
                 reply_markup=None, input_message_content=None):
        InlineQueryResultCachedBase.__init__(self)
        self.type = 'photo'
        self.id = id
        self.photo_file_id = photo_file_id
        self.title = title
        self.description = description
        self.caption = caption
        self.caption_entities = caption_entities
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.parse_mode = parse_mode
        self.payload_dic['photo_file_id'] = photo_file_id


class InlineQueryResultCachedGif(InlineQueryResultCachedBase):
    def __init__(self, id, gif_file_id, title=None, description=None,
                 caption=None, caption_entities=None, parse_mode=None,
                 reply_markup=None, input_message_content=None):
        InlineQueryResultCachedBase.__init__(self)
        self.type = 'gif'
        self.id = id
        self.gif_file_id = gif_file_id
        self.title = title
        self.description = description
        self.caption = caption
        self.caption_entities = caption_entities
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.parse_mode = parse_mode
        self.payload_dic['gif_file_id'] = gif_file_id


class InlineQueryResultCachedMpeg4Gif(InlineQueryResultCachedBase):
    def __init__(self, id, mpeg4_file_id, title=None, description=None,
                 caption=None, caption_entities=None, parse_mode=None,
                 reply_markup=None, input_message_content=None):
        InlineQueryResultCachedBase.__init__(self)
        self.type = 'mpeg4_gif'
        self.id = id
        self.mpeg4_file_id = mpeg4_file_id
        self.title = title
        self.description = description
        self.caption = caption
        self.caption_entities = caption_entities
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.parse_mode = parse_mode
        self.payload_dic['mpeg4_file_id'] = mpeg4_file_id


class InlineQueryResultCachedSticker(InlineQueryResultCachedBase):
    def __init__(self, id, sticker_file_id, reply_markup=None, input_message_content=None):
        InlineQueryResultCachedBase.__init__(self)
        self.type = 'sticker'
        self.id = id
        self.sticker_file_id = sticker_file_id
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.payload_dic['sticker_file_id'] = sticker_file_id


class InlineQueryResultCachedDocument(InlineQueryResultCachedBase):
    def __init__(self, id, document_file_id, title, description=None,
                 caption=None, caption_entities=None, parse_mode=None,
                 reply_markup=None, input_message_content=None):
        InlineQueryResultCachedBase.__init__(self)
        self.type = 'document'
        self.id = id
        self.document_file_id = document_file_id
        self.title = title
        self.description = description
        self.caption = caption
        self.caption_entities = caption_entities
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.parse_mode = parse_mode
        self.payload_dic['document_file_id'] = document_file_id


class InlineQueryResultCachedVideo(InlineQueryResultCachedBase):
    def __init__(self, id, video_file_id, title, description=None,
                 caption=None, caption_entities=None, parse_mode=None,
                 reply_markup=None,
                 input_message_content=None):
        InlineQueryResultCachedBase.__init__(self)
        self.type = 'video'
        self.id = id
        self.video_file_id = video_file_id
        self.title = title
        self.description = description
        self.caption = caption
        self.caption_entities = caption_entities
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.parse_mode = parse_mode
        self.payload_dic['video_file_id'] = video_file_id


class InlineQueryResultCachedVoice(InlineQueryResultCachedBase):
    def __init__(self, id, voice_file_id, title, caption=None, caption_entities=None,
                 parse_mode=None, reply_markup=None, input_message_content=None):
        InlineQueryResultCachedBase.__init__(self)
        self.type = 'voice'
        self.id = id
        self.voice_file_id = voice_file_id
        self.title = title
        self.caption = caption
        self.caption_entities = caption_entities
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.parse_mode = parse_mode
        self.payload_dic['voice_file_id'] = voice_file_id


class InlineQueryResultCachedAudio(InlineQueryResultCachedBase):
    def __init__(self, id, audio_file_id, caption=None, caption_entities=None,
                 parse_mode=None, reply_markup=None, input_message_content=None):
        InlineQueryResultCachedBase.__init__(self)
        self.type = 'audio'
        self.id = id
        self.audio_file_id = audio_file_id
        self.caption = caption
        self.caption_entities = caption_entities
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.parse_mode = parse_mode
        self.payload_dic['audio_file_id'] = audio_file_id
