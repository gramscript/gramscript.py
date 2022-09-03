from abc import ABC
from typing import Optional, Union

from gramscript.types import JsonDeserializable, JsonSerializable


try:
    import ujson as json
except ImportError:
    import json


class BotCommand(JsonSerializable, JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string, dict_copy=False)
        return cls(**obj)

    def __init__(self, command, description):
        """
        This object represents a bot command.
        :param command: Text of the command, 1-32 characters.
            Can contain only lowercase English letters, digits and underscores.
        :param description: Description of the command, 3-256 characters.
        :return:
        """
        self.command: str = command
        self.description: str = description

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {'command': self.command, 'description': self.description}


class BotCommandScope(ABC, JsonSerializable):
    def __init__(self, type='default', chat_id=None, user_id=None):
        """
        Abstract class.
        Use BotCommandScopeX classes to set a specific scope type:
        BotCommandScopeDefault
        BotCommandScopeAllPrivateChats
        BotCommandScopeAllGroupChats
        BotCommandScopeAllChatAdministrators
        BotCommandScopeChat
        BotCommandScopeChatAdministrators
        BotCommandScopeChatMember
        """
        self.type: str = type
        self.chat_id: Optional[Union[int, str]] = chat_id
        self.user_id: Optional[Union[int, str]] = user_id

    def to_json(self):
        json_dict = {'type': self.type}
        if self.chat_id:
            json_dict['chat_id'] = self.chat_id
        if self.user_id:
            json_dict['user_id'] = self.user_id
        return json.dumps(json_dict)


class BotCommandScopeDefault(BotCommandScope):
    def __init__(self):
        """
        Represents the default scope of bot commands.
        Default commands are used if no commands with a narrower scope are specified for the user.
        """
        super(BotCommandScopeDefault, self).__init__(type='default')


class BotCommandScopeAllPrivateChats(BotCommandScope):
    def __init__(self):
        """
        Represents the scope of bot commands, covering all private chats.
        """
        super(BotCommandScopeAllPrivateChats, self).__init__(
            type='all_private_chats')


class BotCommandScopeAllGroupChats(BotCommandScope):
    def __init__(self):
        """
        Represents the scope of bot commands, covering all group and supergroup chats.
        """
        super(BotCommandScopeAllGroupChats, self).__init__(
            type='all_group_chats')


class BotCommandScopeAllChatAdministrators(BotCommandScope):
    def __init__(self):
        """
        Represents the scope of bot commands, covering all group and supergroup chat administrators.
        """
        super(BotCommandScopeAllChatAdministrators, self).__init__(
            type='all_chat_administrators')


class BotCommandScopeChat(BotCommandScope):
    def __init__(self, chat_id=None):
        super(BotCommandScopeChat, self).__init__(type='chat', chat_id=chat_id)


class BotCommandScopeChatAdministrators(BotCommandScope):
    def __init__(self, chat_id=None):
        """
        Represents the scope of bot commands, covering a specific chat.
        @param chat_id: Unique identifier for the target chat
        """
        super(BotCommandScopeChatAdministrators, self).__init__(
            type='chat_administrators', chat_id=chat_id)


class BotCommandScopeChatMember(BotCommandScope):
    def __init__(self, chat_id=None, user_id=None):
        """
        Represents the scope of bot commands, covering all administrators of a specific group or supergroup chat
        @param chat_id: Unique identifier for the target chat
        @param user_id: Unique identifier of the target user
        """
        super(BotCommandScopeChatMember, self).__init__(
            type='chat_member', chat_id=chat_id, user_id=user_id)
