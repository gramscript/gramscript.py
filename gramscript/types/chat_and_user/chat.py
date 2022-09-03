try:
    import ujson as json
except ImportError:
    import json

from typing import Dict, List, Optional
from gramscript.callback.callback import CallbackQuery
from gramscript.inline.InlineQuery import ChosenInlineResult, InlineQuery
from gramscript.types.payment.payment import PreCheckoutQuery, ShippingQuery

from gramscript.types.poll.poll import Poll, PollAnswer
from ..media import Location
from ..message import Message
from ..object import Dictionaryable, JsonDeserializable, JsonSerializable
from .user import User


class Chat(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string)
        if 'photo' in obj:
            obj['photo'] = ChatPhoto.de_json(obj['photo'])
        if 'pinned_message' in obj:
            obj['pinned_message'] = Message.de_json(obj['pinned_message'])
        if 'permissions' in obj:
            obj['permissions'] = ChatPermissions.de_json(obj['permissions'])
        if 'location' in obj:
            obj['location'] = ChatLocation.de_json(obj['location'])
        return cls(**obj)

    def __init__(self, id, type, title=None, username=None, first_name=None,
                 last_name=None, photo=None, bio=None, has_private_forwards=None,
                 description=None, invite_link=None, pinned_message=None,
                 permissions=None, slow_mode_delay=None,
                 message_auto_delete_time=None, has_protected_content=None, sticker_set_name=None,
                 can_set_sticker_set=None, linked_chat_id=None, location=None, **kwargs):
        self.id: int = id
        self.type: str = type
        self.title: str = title
        self.username: str = username
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.photo: ChatPhoto = photo
        self.bio: str = bio
        self.has_private_forwards: bool = has_private_forwards
        self.description: str = description
        self.invite_link: str = invite_link
        self.pinned_message: Message = pinned_message
        self.permissions: ChatPermissions = permissions
        self.slow_mode_delay: int = slow_mode_delay
        self.message_auto_delete_time: int = message_auto_delete_time
        self.has_protected_content: bool = has_protected_content
        self.sticker_set_name: str = sticker_set_name
        self.can_set_sticker_set: bool = can_set_sticker_set
        self.linked_chat_id: int = linked_chat_id
        self.location: ChatLocation = location


class ChatPhoto(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string, dict_copy=False)
        return cls(**obj)

    def __init__(self, small_file_id, small_file_unique_id, big_file_id, big_file_unique_id, **kwargs):
        self.small_file_id: str = small_file_id
        self.small_file_unique_id: str = small_file_unique_id
        self.big_file_id: str = big_file_id
        self.big_file_unique_id: str = big_file_unique_id


class ChatMember(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string)
        obj['user'] = User.de_json(obj['user'])
        return cls(**obj)

    def __init__(self, user, status, custom_title=None, is_anonymous=None, can_be_edited=None,
                 can_post_messages=None, can_edit_messages=None, can_delete_messages=None,
                 can_restrict_members=None, can_promote_members=None, can_change_info=None,
                 can_invite_users=None,  can_pin_messages=None, is_member=None,
                 can_send_messages=None, can_send_media_messages=None, can_send_polls=None,
                 can_send_other_messages=None, can_add_web_page_previews=None,
                 can_manage_chat=None, can_manage_voice_chats=None,
                 until_date=None, **kwargs):
        self.user: User = user
        self.status: str = status
        self.custom_title: str = custom_title
        self.is_anonymous: bool = is_anonymous
        self.can_be_edited: bool = can_be_edited
        self.can_post_messages: bool = can_post_messages
        self.can_edit_messages: bool = can_edit_messages
        self.can_delete_messages: bool = can_delete_messages
        self.can_restrict_members: bool = can_restrict_members
        self.can_promote_members: bool = can_promote_members
        self.can_change_info: bool = can_change_info
        self.can_invite_users: bool = can_invite_users
        self.can_pin_messages: bool = can_pin_messages
        self.is_member: bool = is_member
        self.can_send_messages: bool = can_send_messages
        self.can_send_media_messages: bool = can_send_media_messages
        self.can_send_polls: bool = can_send_polls
        self.can_send_other_messages: bool = can_send_other_messages
        self.can_add_web_page_previews: bool = can_add_web_page_previews
        self.can_manage_chat: bool = can_manage_chat
        self.can_manage_voice_chats: bool = can_manage_voice_chats
        self.until_date: int = until_date


class ChatInviteLink(JsonSerializable, JsonDeserializable, Dictionaryable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string)
        obj['creator'] = User.de_json(obj['creator'])
        return cls(**obj)

    def __init__(self, invite_link, creator, creates_join_request, is_primary, is_revoked,
                 name=None, expire_date=None, member_limit=None, pending_join_request_count=None, **kwargs):
        self.invite_link: str = invite_link
        self.creator: User = creator
        self.creates_join_request: bool = creates_join_request
        self.is_primary: bool = is_primary
        self.is_revoked: bool = is_revoked
        self.name: str = name
        self.expire_date: int = expire_date
        self.member_limit: int = member_limit
        self.pending_join_request_count: int = pending_join_request_count

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        json_dict = {
            "invite_link": self.invite_link,
            "creator": self.creator.to_dict(),
            "is_primary": self.is_primary,
            "is_revoked": self.is_revoked,
            "creates_join_request": self.creates_join_request
        }
        if self.expire_date:
            json_dict["expire_date"] = self.expire_date
        if self.member_limit:
            json_dict["member_limit"] = self.member_limit
        if self.pending_join_request_count:
            json_dict["pending_join_request_count"] = self.pending_join_request_count
        if self.name:
            json_dict["name"] = self.name
        return json_dict


class ChatJoinRequest(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string)
        obj['chat'] = Chat.de_json(obj['chat'])
        obj['from_user'] = User.de_json(obj['from'])
        obj['invite_link'] = ChatInviteLink.de_json(obj.get('invite_link'))
        return cls(**obj)

    def __init__(self, chat, from_user, date, bio=None, invite_link=None, **kwargs):
        self.chat = chat
        self.from_user = from_user
        self.date = date
        self.bio = bio
        self.invite_link = invite_link


class ChatPermissions(JsonDeserializable, JsonSerializable, Dictionaryable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return json_string
        obj = cls.check_json(json_string, dict_copy=False)
        return cls(**obj)

    def __init__(self, can_send_messages=None, can_send_media_messages=None,
                 can_send_polls=None, can_send_other_messages=None,
                 can_add_web_page_previews=None, can_change_info=None,
                 can_invite_users=None, can_pin_messages=None, **kwargs):
        self.can_send_messages: bool = can_send_messages
        self.can_send_media_messages: bool = can_send_media_messages
        self.can_send_polls: bool = can_send_polls
        self.can_send_other_messages: bool = can_send_other_messages
        self.can_add_web_page_previews: bool = can_add_web_page_previews
        self.can_change_info: bool = can_change_info
        self.can_invite_users: bool = can_invite_users
        self.can_pin_messages: bool = can_pin_messages

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        json_dict = {}
        if self.can_send_messages is not None:
            json_dict['can_send_messages'] = self.can_send_messages
        if self.can_send_media_messages is not None:
            json_dict['can_send_media_messages'] = self.can_send_media_messages
        if self.can_send_polls is not None:
            json_dict['can_send_polls'] = self.can_send_polls
        if self.can_send_other_messages is not None:
            json_dict['can_send_other_messages'] = self.can_send_other_messages
        if self.can_add_web_page_previews is not None:
            json_dict['can_add_web_page_previews'] = self.can_add_web_page_previews
        if self.can_change_info is not None:
            json_dict['can_change_info'] = self.can_change_info
        if self.can_invite_users is not None:
            json_dict['can_invite_users'] = self.can_invite_users
        if self.can_pin_messages is not None:
            json_dict['can_pin_messages'] = self.can_pin_messages
        return json_dict


class ChatLocation(JsonSerializable, JsonDeserializable, Dictionaryable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return json_string
        obj = cls.check_json(json_string)
        obj['location'] = Location.de_json(obj['location'])
        return cls(**obj)

    def __init__(self, location, address, **kwargs):
        self.location: Location = location
        self.address: str = address

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            "location": self.location.to_dict(),
            "address": self.address
        }


class Update(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string, dict_copy=False)
        update_id = obj['update_id']
        message = Message.de_json(obj.get('message'))
        edited_message = Message.de_json(obj.get('edited_message'))
        channel_post = Message.de_json(obj.get('channel_post'))
        edited_channel_post = Message.de_json(obj.get('edited_channel_post'))
        inline_query = InlineQuery.de_json(obj.get('inline_query'))
        chosen_inline_result = ChosenInlineResult.de_json(
            obj.get('chosen_inline_result'))
        callback_query = CallbackQuery.de_json(obj.get('callback_query'))
        shipping_query = ShippingQuery.de_json(obj.get('shipping_query'))
        pre_checkout_query = PreCheckoutQuery.de_json(
            obj.get('pre_checkout_query'))
        poll = Poll.de_json(obj.get('poll'))
        poll_answer = PollAnswer.de_json(obj.get('poll_answer'))
        my_chat_member = ChatMemberUpdated.de_json(obj.get('my_chat_member'))
        chat_member = ChatMemberUpdated.de_json(obj.get('chat_member'))
        chat_join_request = ChatJoinRequest.de_json(
            obj.get('chat_join_request'))
        return cls(update_id, message, edited_message, channel_post, edited_channel_post, inline_query,
                   chosen_inline_result, callback_query, shipping_query, pre_checkout_query, poll, poll_answer,
                   my_chat_member, chat_member, chat_join_request)

    def __init__(self, update_id, message, edited_message, channel_post, edited_channel_post, inline_query,
                 chosen_inline_result, callback_query, shipping_query, pre_checkout_query, poll, poll_answer,
                 my_chat_member, chat_member, chat_join_request):
        self.update_id = update_id
        self.message = message
        self.edited_message = edited_message
        self.channel_post = channel_post
        self.edited_channel_post = edited_channel_post
        self.inline_query = inline_query
        self.chosen_inline_result = chosen_inline_result
        self.callback_query = callback_query
        self.shipping_query = shipping_query
        self.pre_checkout_query = pre_checkout_query
        self.poll = poll
        self.poll_answer = poll_answer
        self.my_chat_member = my_chat_member
        self.chat_member = chat_member
        self.chat_join_request = chat_join_request


class ChatMemberUpdated(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string)
        obj['chat'] = Chat.de_json(obj['chat'])
        obj['from_user'] = User.de_json(obj.pop('from'))
        obj['old_chat_member'] = ChatMember.de_json(obj['old_chat_member'])
        obj['new_chat_member'] = ChatMember.de_json(obj['new_chat_member'])
        obj['invite_link'] = ChatInviteLink.de_json(obj.get('invite_link'))
        return cls(**obj)

    def __init__(self, chat, from_user, date, old_chat_member, new_chat_member, invite_link=None, **kwargs):
        self.chat: Chat = chat
        self.from_user: User = from_user
        self.date: int = date
        self.old_chat_member: ChatMember = old_chat_member
        self.new_chat_member: ChatMember = new_chat_member
        self.invite_link: Optional[ChatInviteLink] = invite_link

    @property
    def difference(self) -> Dict[str, List]:
        """
        Get the difference between `old_chat_member` and `new_chat_member`
        as a dict in the following format {'parameter': [old_value, new_value]}
        E.g {'status': ['member', 'kicked'], 'until_date': [None, 1625055092]} 
        """
        old: Dict = self.old_chat_member.__dict__
        new: Dict = self.new_chat_member.__dict__
        dif = {}
        for key in new:
            if key == 'user':
                continue
            if new[key] != old[key]:
                dif[key] = [old[key], new[key]]
        return dif
