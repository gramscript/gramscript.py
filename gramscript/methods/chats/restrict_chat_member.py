from gramscript.scaffold import Scaffold
from gramscript import types
from gramscript import raw
from typing import Union
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


class RestrictChatMember(Scaffold):
    async def restrict_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: Union[int, str],
        permissions: "types.ChatPermissions",
        until_date: int = 0
    ) -> "types.Chat":
        """Restrict a user in a supergroup.

        You must be an administrator in the supergroup for this to work and must have the appropriate admin rights.
        Pass True for all permissions to lift restrictions from a user.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            permissions (:obj:`~gramscript.types.ChatPermissions`):
                New user permissions.

            until_date (``int``, *optional*):
                Date when the user will be unbanned, unix time.
                If user is banned for more than 366 days or less than 30 seconds from the current time they are
                considered to be banned forever. Defaults to 0 (ban forever).

        Returns:
            :obj:`~gramscript.types.Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                from time import time

                from gramscript import ChatPermissions

                # Completely restrict chat member (mute) forever
                app.restrict_chat_member(chat_id, user_id, ChatPermissions())

                # Chat member muted for 24h
                app.restrict_chat_member(chat_id, user_id, ChatPermissions(), int(time() + 86400))

                # Chat member can only send text messages
                app.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=True))
        """
        r = await self.send(
            raw.functions.channels.EditBanned(
                channel=await self.resolve_peer(chat_id),
                user_id=await self.resolve_peer(user_id),
                banned_rights=raw.types.ChatBannedRights(
                    until_date=until_date,
                    send_messages=True if not permissions.can_send_messages else None,
                    send_media=True if not permissions.can_send_media_messages else None,
                    send_stickers=True if not permissions.can_send_stickers else None,
                    send_gifs=True if not permissions.can_send_animations else None,
                    send_games=True if not permissions.can_send_games else None,
                    send_inline=True if not permissions.can_use_inline_bots else None,
                    embed_links=True if not permissions.can_add_web_page_previews else None,
                    send_polls=True if not permissions.can_send_polls else None,
                    change_info=True if not permissions.can_change_info else None,
                    invite_users=True if not permissions.can_invite_users else None,
                    pin_messages=True if not permissions.can_pin_messages else None,
                )
            )
        )

        return types.Chat._parse_chat(self, r.chats[0])
