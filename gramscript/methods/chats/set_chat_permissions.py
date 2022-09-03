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


class SetChatPermissions(Scaffold):
    async def set_chat_permissions(
        self,
        chat_id: Union[int, str],
        permissions: "types.ChatPermissions",
    ) -> "types.Chat":
        """Set default chat permissions for all members.

        You must be an administrator in the group or a supergroup for this to work and must have the
        *can_restrict_members* admin rights.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            permissions (:obj:`~gramscript.types.ChatPermissions`):
                New default chat permissions.

        Returns:
            :obj:`~gramscript.types.Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                from gramscript import ChatPermissions

                # Completely restrict chat
                app.set_chat_permissions(chat_id, ChatPermissions())

                # Chat members can only send text messages, media, stickers and GIFs
                app.set_chat_permissions(
                    chat_id,
                    ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_stickers=True,
                        can_send_animations=True
                    )
                )
        """
        r = await self.send(
            raw.functions.messages.EditChatDefaultBannedRights(
                peer=await self.resolve_peer(chat_id),
                banned_rights=raw.types.ChatBannedRights(
                    until_date=0,
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
