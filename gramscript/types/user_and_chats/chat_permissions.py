from ..object import Object
from gramscript import raw
# MIT License

# Copyright (c) 2022 Gramscript Telegram API

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class ChatPermissions(Object):
    """A chat default permissions and a single member permissions within a chat.

    Some permissions make sense depending on the context: default chat permissions, restricted/kicked member or
    administrators in groups or channels.

    .. note::

        gramscript's chat permission are much more detailed. In particular, you can restrict sending stickers, animations,
        games and inline bot results individually, allowing a finer control.

        If you wish to have the same permissions as seen in official apps or in bot API's *"can_send_other_messages"*
        simply set these arguments to True: ``can_send_stickers``, ``can_send_animations``, ``can_send_games`` and
        ``can_use_inline_bots``.

    Parameters:
        can_send_messages (``bool``, *optional*):
            True, if the user is allowed to send text messages, contacts, locations and venues.

        can_send_media_messages (``bool``, *optional*):
            True, if the user is allowed to send audios, documents, photos, videos, video notes and voice notes, implies
            can_send_messages.

        can_send_stickers (``bool``, *optional*):
            True, if the user is allowed to send stickers, implies can_send_media_messages.

        can_send_animations (``bool``, *optional*):
            True, if the user is allowed to send animations (GIFs), implies can_send_media_messages.

        can_send_games (``bool``, *optional*):
            True, if the user is allowed to send games, implies can_send_media_messages.

        can_use_inline_bots (``bool``, *optional*):
            True, if the user is allowed to use inline bots, implies can_send_media_messages.

        can_add_web_page_previews (``bool``, *optional*):
            True, if the user is allowed to add web page previews to their messages, implies can_send_media_messages.

        can_send_polls (``bool``, *optional*):
            True, if the user is allowed to send polls, implies can_send_messages.

        can_change_info (``bool``, *optional*):
            True, if the user is allowed to change the chat title, photo and other settings.
            Ignored in public supergroups.

        can_invite_users (``bool``, *optional*):
            True, if the user is allowed to invite new users to the chat.

        can_pin_messages (``bool``, *optional*):
            True, if the user is allowed to pin messages.
            Ignored in public supergroups.
    """

    def __init__(
        self,
        *,
        can_send_messages: bool = None,  # Text, contacts, locations and venues
        # Audios, documents, photos, videos, video notes and voice notes
        can_send_media_messages: bool = None,
        can_send_stickers: bool = None,
        can_send_animations: bool = None,
        can_send_games: bool = None,
        can_use_inline_bots: bool = None,
        can_add_web_page_previews: bool = None,
        can_send_polls: bool = None,
        can_change_info: bool = None,
        can_invite_users: bool = None,
        can_pin_messages: bool = None
    ):
        super().__init__(None)

        self.can_send_messages = can_send_messages
        self.can_send_media_messages = can_send_media_messages
        self.can_send_stickers = can_send_stickers
        self.can_send_animations = can_send_animations
        self.can_send_games = can_send_games
        self.can_use_inline_bots = can_use_inline_bots
        self.can_add_web_page_previews = can_add_web_page_previews
        self.can_send_polls = can_send_polls
        self.can_change_info = can_change_info
        self.can_invite_users = can_invite_users
        self.can_pin_messages = can_pin_messages

    @staticmethod
    def _parse(denied_permissions: "raw.types.ChatBannedRights") -> "ChatPermissions":
        if isinstance(denied_permissions, raw.types.ChatBannedRights):
            return ChatPermissions(
                can_send_messages=not denied_permissions.send_messages,
                can_send_media_messages=not denied_permissions.send_media,
                can_send_stickers=not denied_permissions.send_stickers,
                can_send_animations=not denied_permissions.send_gifs,
                can_send_games=not denied_permissions.send_games,
                can_use_inline_bots=not denied_permissions.send_inline,
                can_add_web_page_previews=not denied_permissions.embed_links,
                can_send_polls=not denied_permissions.send_polls,
                can_change_info=not denied_permissions.change_info,
                can_invite_users=not denied_permissions.invite_users,
                can_pin_messages=not denied_permissions.pin_messages
            )
