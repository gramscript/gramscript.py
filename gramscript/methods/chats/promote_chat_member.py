from gramscript.scaffold import Scaffold
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


class PromoteChatMember(Scaffold):
    async def promote_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: Union[int, str],
        can_change_info: bool = True,
        can_post_messages: bool = False,
        can_edit_messages: bool = False,
        can_delete_messages: bool = True,
        can_restrict_members: bool = True,
        can_invite_users: bool = True,
        can_pin_messages: bool = False,
        can_promote_members: bool = False
    ) -> bool:
        """Promote or demote a user in a supergroup or a channel.

        You must be an administrator in the chat for this to work and must have the appropriate admin rights.
        Pass False for all boolean parameters to demote a user.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            can_change_info (``bool``, *optional*):
                Pass True, if the administrator can change chat title, photo and other settings.

            can_post_messages (``bool``, *optional*):
                Pass True, if the administrator can create channel posts, channels only.

            can_edit_messages (``bool``, *optional*):
                Pass True, if the administrator can edit messages of other users and can pin messages, channels only.

            can_delete_messages (``bool``, *optional*):
                Pass True, if the administrator can delete messages of other users.

            can_restrict_members (``bool``, *optional*):
                Pass True, if the administrator can restrict, ban or unban chat members.

            can_invite_users (``bool``, *optional*):
                Pass True, if the administrator can invite new users to the chat.

            can_pin_messages (``bool``, *optional*):
                Pass True, if the administrator can pin messages, supergroups only.

            can_promote_members (``bool``, *optional*):
                Pass True, if the administrator can add new administrators with a subset of his own privileges or
                demote administrators that he has promoted, directly or indirectly (promoted by administrators that
                were appointed by him).

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Promote chat member to supergroup admin
                app.promote_chat_member(chat_id, user_id)
        """
        await self.send(
            raw.functions.channels.EditAdmin(
                channel=await self.resolve_peer(chat_id),
                user_id=await self.resolve_peer(user_id),
                admin_rights=raw.types.ChatAdminRights(
                    change_info=can_change_info or None,
                    post_messages=can_post_messages or None,
                    edit_messages=can_edit_messages or None,
                    delete_messages=can_delete_messages or None,
                    ban_users=can_restrict_members or None,
                    invite_users=can_invite_users or None,
                    pin_messages=can_pin_messages or None,
                    add_admins=can_promote_members or None,
                ),
                rank=""
            )
        )

        return True
