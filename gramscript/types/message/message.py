try:
    import ujson as json
except ImportError:
    import json
from typing import Dict, List, Optional, Union

from ..game import Animation, Game
from ..media import Audio, Contact, Dice, Document, Location, Venue, Video, VideoNote, PhotoSize
from ..sticker import Sticker
from ..chat_and_user import Chat, User
from ..object import Dictionaryable, JsonDeserializable, JsonSerializable


class MessageID(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string, dict_copy=False)
        return cls(**obj)

    def __init__(self, message_id, **kwargs):
        self.message_id = message_id


class Message(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string, dict_copy=False)
        message_id = obj['message_id']
        from_user = User.de_json(obj.get('from'))
        date = obj['date']
        chat = Chat.de_json(obj['chat'])
        content_type = None
        opts = {}
        if 'sender_chat' in obj:
            opts['sender_chat'] = Chat.de_json(obj['sender_chat'])
        if 'forward_from' in obj:
            opts['forward_from'] = User.de_json(obj['forward_from'])
        if 'forward_from_chat' in obj:
            opts['forward_from_chat'] = Chat.de_json(obj['forward_from_chat'])
        if 'forward_from_message_id' in obj:
            opts['forward_from_message_id'] = obj.get(
                'forward_from_message_id')
        if 'forward_signature' in obj:
            opts['forward_signature'] = obj.get('forward_signature')
        if 'forward_sender_name' in obj:
            opts['forward_sender_name'] = obj.get('forward_sender_name')
        if 'forward_date' in obj:
            opts['forward_date'] = obj.get('forward_date')
        if 'is_automatic_forward' in obj:
            opts['is_automatic_forward'] = obj.get('is_automatic_forward')
        if 'reply_to_message' in obj:
            opts['reply_to_message'] = Message.de_json(obj['reply_to_message'])
        if 'via_bot' in obj:
            opts['via_bot'] = User.de_json(obj['via_bot'])
        if 'edit_date' in obj:
            opts['edit_date'] = obj.get('edit_date')
        if 'has_protected_content' in obj:
            opts['has_protected_content'] = obj.get('has_protected_content')
        if 'media_group_id' in obj:
            opts['media_group_id'] = obj.get('media_group_id')
        if 'author_signature' in obj:
            opts['author_signature'] = obj.get('author_signature')
        if 'text' in obj:
            opts['text'] = obj['text']
            content_type = 'text'
        if 'entities' in obj:
            opts['entities'] = Message.parse_entities(obj['entities'])
        if 'caption_entities' in obj:
            opts['caption_entities'] = Message.parse_entities(
                obj['caption_entities'])
        if 'audio' in obj:
            opts['audio'] = Audio.de_json(obj['audio'])
            content_type = 'audio'
        if 'document' in obj:
            opts['document'] = Document.de_json(obj['document'])
            content_type = 'document'
        if 'animation' in obj:
            opts['animation'] = Animation.de_json(obj['animation'])
            content_type = 'animation'
        if 'game' in obj:
            opts['game'] = Game.de_json(obj['game'])
            content_type = 'game'
        if 'photo' in obj:
            opts['photo'] = Message.parse_photo(obj['photo'])
            content_type = 'photo'
        if 'sticker' in obj:
            opts['sticker'] = Sticker.de_json(obj['sticker'])
            content_type = 'sticker'
        if 'video' in obj:
            opts['video'] = Video.de_json(obj['video'])
            content_type = 'video'
        if 'video_note' in obj:
            opts['video_note'] = VideoNote.de_json(obj['video_note'])
            content_type = 'video_note'
        if 'voice' in obj:
            opts['voice'] = Audio.de_json(obj['voice'])
            content_type = 'voice'
        if 'caption' in obj:
            opts['caption'] = obj['caption']
        if 'contact' in obj:
            opts['contact'] = Contact.de_json(json.dumps(obj['contact']))
            content_type = 'contact'
        if 'location' in obj:
            opts['location'] = Location.de_json(obj['location'])
            content_type = 'location'
        if 'venue' in obj:
            opts['venue'] = Venue.de_json(obj['venue'])
            content_type = 'venue'
        if 'dice' in obj:
            opts['dice'] = Dice.de_json(obj['dice'])
            content_type = 'dice'
        if 'new_chat_members' in obj:
            new_chat_members = [User.de_json(member)
                                for member in obj['new_chat_members']]
            opts['new_chat_members'] = new_chat_members
            content_type = 'new_chat_members'
        if 'left_chat_member' in obj:
            opts['left_chat_member'] = User.de_json(obj['left_chat_member'])
            content_type = 'left_chat_member'
        if 'new_chat_title' in obj:
            opts['new_chat_title'] = obj['new_chat_title']
            content_type = 'new_chat_title'
        if 'new_chat_photo' in obj:
            opts['new_chat_photo'] = Message.parse_photo(obj['new_chat_photo'])
            content_type = 'new_chat_photo'
        if 'delete_chat_photo' in obj:
            opts['delete_chat_photo'] = obj['delete_chat_photo']
            content_type = 'delete_chat_photo'
        if 'group_chat_created' in obj:
            opts['group_chat_created'] = obj['group_chat_created']
            content_type = 'group_chat_created'
        if 'supergroup_chat_created' in obj:
            opts['supergroup_chat_created'] = obj['supergroup_chat_created']
            content_type = 'supergroup_chat_created'
        if 'channel_chat_created' in obj:
            opts['channel_chat_created'] = obj['channel_chat_created']
            content_type = 'channel_chat_created'
        if 'migrate_to_chat_id' in obj:
            opts['migrate_to_chat_id'] = obj['migrate_to_chat_id']
            content_type = 'migrate_to_chat_id'
        if 'migrate_from_chat_id' in obj:
            opts['migrate_from_chat_id'] = obj['migrate_from_chat_id']
            content_type = 'migrate_from_chat_id'
        if 'pinned_message' in obj:
            opts['pinned_message'] = Message.de_json(obj['pinned_message'])
            content_type = 'pinned_message'
        if 'invoice' in obj:
            opts['invoice'] = Invoice.de_json(obj['invoice'])
            content_type = 'invoice'
        if 'successful_payment' in obj:
            opts['successful_payment'] = SuccessfulPayment.de_json(
                obj['successful_payment'])

            content_type = 'successful_payment'
        if 'connected_website' in obj:
            opts['connected_website'] = obj['connected_website']
            content_type = 'connected_website'
        if 'poll' in obj:
            opts['poll'] = Poll.de_json(obj['poll'])
            content_type = 'poll'
        if 'passport_data' in obj:
            opts['passport_data'] = obj['passport_data']
            content_type = 'passport_data'
        if 'proximity_alert_triggered' in obj:
            opts['proximity_alert_triggered'] = ProximityAlertTriggered.de_json(
                obj['proximity_alert_triggered'])

            content_type = 'proximity_alert_triggered'
        if 'voice_chat_scheduled' in obj:
            opts['voice_chat_scheduled'] = VoiceChatScheduled.de_json(
                obj['voice_chat_scheduled'])

            content_type = 'voice_chat_scheduled'
        if 'voice_chat_started' in obj:
            opts['voice_chat_started'] = VoiceChatStarted.de_json(
                obj['voice_chat_started'])

            content_type = 'voice_chat_started'
        if 'voice_chat_ended' in obj:
            opts['voice_chat_ended'] = VoiceChatEnded.de_json(
                obj['voice_chat_ended'])
            content_type = 'voice_chat_ended'
        if 'voice_chat_participants_invited' in obj:
            opts['voice_chat_participants_invited'] = VoiceChatParticipantsInvited.de_json(
                obj['voice_chat_participants_invited'])

            content_type = 'voice_chat_participants_invited'
        if 'message_auto_delete_timer_changed' in obj:
            opts['message_auto_delete_timer_changed'] = MessageAutoDeleteTimerChanged.de_json(
                obj['message_auto_delete_timer_changed'])

            content_type = 'message_auto_delete_timer_changed'
        if 'reply_markup' in obj:
            opts['reply_markup'] = InlineKeyboardMarkup.de_json(
                obj['reply_markup'])
        return cls(message_id, from_user, date, chat, content_type, opts, json_string)

    @classmethod
    def parse_chat(cls, chat):
        return User.de_json(chat) if 'first_name' in chat else GroupChat.de_json(chat)

    @classmethod
    def parse_photo(cls, photo_size_array):
        return [PhotoSize.de_json(ps) for ps in photo_size_array]

    @classmethod
    def parse_entities(cls, message_entity_array):
        return [MessageEntity.de_json(me) for me in message_entity_array]

    def __init__(self, message_id, from_user, date, chat, content_type, options, json_string):
        self.content_type: str = content_type
        # Lets fix the telegram usability ####up with ID in Message :)
        self.id: int = message_id
        self.message_id: int = message_id
        self.from_user: User = from_user
        self.date: int = date
        self.chat: Chat = chat
        self.sender_chat: Optional[Chat] = None
        self.forward_from: Optional[User] = None
        self.forward_from_chat: Optional[Chat] = None
        self.forward_from_message_id: Optional[int] = None
        self.forward_signature: Optional[str] = None
        self.forward_sender_name: Optional[str] = None
        self.forward_date: Optional[int] = None
        self.is_automatic_forward: Optional[bool] = None
        self.reply_to_message: Optional[Message] = None
        self.via_bot: Optional[User] = None
        self.edit_date: Optional[int] = None
        self.has_protected_content: Optional[bool] = None
        self.media_group_id: Optional[str] = None
        self.author_signature: Optional[str] = None
        self.text: Optional[str] = None
        self.entities: Optional[List[MessageEntity]] = None
        self.caption_entities: Optional[List[MessageEntity]] = None
        self.audio: Optional[Audio] = None
        self.document: Optional[Document] = None
        self.photo: Optional[List[PhotoSize]] = None
        self.sticker: Optional[Sticker] = None
        self.video: Optional[Video] = None
        self.video_note: Optional[VideoNote] = None
        self.voice: Optional[Voice] = None
        self.caption: Optional[str] = None
        self.contact: Optional[Contact] = None
        self.location: Optional[Location] = None
        self.venue: Optional[Venue] = None
        self.animation: Optional[Animation] = None
        self.dice: Optional[Dice] = None
        # Deprecated since Bot API 3.0. Not processed anymore
        self.new_chat_member: Optional[User] = None
        self.new_chat_members: Optional[List[User]] = None
        self.left_chat_member: Optional[User] = None
        self.new_chat_title: Optional[str] = None
        self.new_chat_photo: Optional[List[PhotoSize]] = None
        self.delete_chat_photo: Optional[bool] = None
        self.group_chat_created: Optional[bool] = None
        self.supergroup_chat_created: Optional[bool] = None
        self.channel_chat_created: Optional[bool] = None
        self.migrate_to_chat_id: Optional[int] = None
        self.migrate_from_chat_id: Optional[int] = None
        self.pinned_message: Optional[Message] = None
        self.invoice: Optional[Invoice] = None
        self.successful_payment: Optional[SuccessfulPayment] = None
        self.connected_website: Optional[str] = None
        self.reply_markup: Optional[InlineKeyboardMarkup] = None
        for key in options:
            setattr(self, key, options[key])
        self.json = json_string

    def __html_text(self, text, entities):
        """
        Author: @sviat9440
        Updaters: @badiboy
        Message: "*Test* parse _formatting_, [url](https://example.com), [text_mention](tg://user?id=123456) and mention @username"

        Example:
            message.html_text
            >> "<b>Test</b> parse <i>formatting</i>, <a href=\"https://example.com\">url</a>, <a href=\"tg://user?id=123456\">text_mention</a> and mention @username"

        Custom subs:
            You can customize the substitutes. By default, there is no substitute for the entities: hashtag, bot_command, email. You can add or modify substitute an existing entity.
        Example:
            message.custom_subs = {"bold": "<strong class=\"example\">{text}</strong>", "italic": "<i class=\"example\">{text}</i>", "mention": "<a href={url}>{text}</a>"}
            message.html_text
            >> "<strong class=\"example\">Test</strong> parse <i class=\"example\">formatting</i>, <a href=\"https://example.com\">url</a> and <a href=\"tg://user?id=123456\">text_mention</a> and mention <a href=\"https://t.me/username\">@username</a>"
        """

        if not entities:
            return text

        _subs = {
            "bold": "<b>{text}</b>",
            "italic": "<i>{text}</i>",
            "pre": "<pre>{text}</pre>",
            "code": "<code>{text}</code>",
            # "url": "<a href=\"{url}\">{text}</a>", # @badiboy plain URLs have no text and do not need tags
            "text_link": "<a href=\"{url}\">{text}</a>",
            "strikethrough": "<s>{text}</s>",
            "underline":     "<u>{text}</u>",
            "spoiler": "<span class=\"tg-spoiler\">{text}</span>",
        }

        if hasattr(self, "custom_subs"):
            for key, value in self.custom_subs.items():
                _subs[key] = value
        utf16_text = text.encode("utf-16-le")
        html_text = ""

        def func(upd_text, subst_type=None, url=None, user=None):
            upd_text = upd_text.decode("utf-16-le")
            if subst_type == "text_mention":
                subst_type = "text_link"
                url = "tg://user?id={0}".format(user.id)
            elif subst_type == "mention":
                url = "https://t.me/{0}".format(upd_text[1:])
            upd_text = upd_text.replace("&", "&amp;").replace(
                "<", "&lt;").replace(">", "&gt;")
            if not subst_type or not _subs.get(subst_type):
                return upd_text
            subs = _subs.get(subst_type)
            return subs.format(text=upd_text, url=url)

        offset = 0
        for entity in entities:
            if entity.offset > offset:
                html_text += func(utf16_text[offset * 2: entity.offset * 2])
                offset = entity.offset
                html_text += func(utf16_text[offset * 2: (offset + entity.length)
                                  * 2], entity.type, entity.url, entity.user)
                offset += entity.length
            elif entity.offset == offset:
                html_text += func(utf16_text[offset * 2: (offset + entity.length)
                                  * 2], entity.type, entity.url, entity.user)
                offset += entity.length
        if offset * 2 < len(utf16_text):
            html_text += func(utf16_text[offset * 2:])
        return html_text

    @property
    def html_text(self):
        return self.__html_text(self.text, self.entities)

    @property
    def html_caption(self):
        return self.__html_text(self.caption, self.caption_entities)


class MessageEntity(Dictionaryable, JsonSerializable, JsonDeserializable):
    @staticmethod
    def to_list_of_dicts(entity_list) -> Union[List[Dict], None]:
        res = [MessageEntity.to_dict(e) for e in entity_list]
        return res or None

    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string)
        if 'user' in obj:
            obj['user'] = User.de_json(obj['user'])
        return cls(**obj)

    def __init__(self, type, offset, length, url=None, user=None, language=None, **kwargs):
        self.type: str = type
        self.offset: int = offset
        self.length: int = length
        self.url: str = url
        self.user: User = user
        self.language: str = language

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {"type": self.type,
                "offset": self.offset,
                "length": self.length,
                "url": self.url,
                "user": self.user,
                "language":  self.language}


class MessageAutoDeleteTimerChanged(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string, dict_copy=False)
        return cls(**obj)

    def __init__(self, message_auto_delete_time, **kwargs):
        self.message_auto_delete_time = message_auto_delete_time


class ForceReply(JsonSerializable):
    def __init__(self, selective: Optional[bool] = None, input_field_placeholder: Optional[str] = None):
        self.selective: bool = selective
        self.input_field_placeholder: str = input_field_placeholder

    def to_json(self):
        json_dict = {'force_reply': True}
        if self.selective is not None:
            json_dict['selective'] = self.selective
        if self.input_field_placeholder:
            json_dict['input_field_placeholder'] = self.input_field_placeholder
        return json.dumps(json_dict)
