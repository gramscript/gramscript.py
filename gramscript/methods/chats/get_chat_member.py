from gramscript.scaffold import Scaffold
from gramscript.errors import UserNotParticipant
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


class GetChatMember(Scaffold):
    async def get_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: Union[int, str]
    ) -> "types.ChatMember":
        """Get information about one member of a chat.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            user_id (``int`` | ``str``)::
                Unique identifier (int) or username (str) of the target user.
                For you yourself you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

        Returns:
            :obj:`~gramscript.types.ChatMember`: On success, a chat member is returned.

        Example:
            .. code-block:: python

                dan = app.get_chat_member("gramscriptchat", "haskell")
                print(dan)
        """
        chat = await self.resolve_peer(chat_id)
        user = await self.resolve_peer(user_id)

        if isinstance(chat, raw.types.InputPeerChat):
            r = await self.send(
                raw.functions.messages.GetFullChat(
                    chat_id=chat.chat_id
                )
            )

            members = getattr(r.full_chat.participants, "participants", [])
            users = {i.id: i for i in r.users}

            for member in members:
                member = types.ChatMember._parse(self, member, users)

                if isinstance(user, raw.types.InputPeerSelf):
                    if member.user.is_self:
                        return member
                else:
                    if member.user.id == user.user_id:
                        return member
            else:
                raise UserNotParticipant
        elif isinstance(chat, raw.types.InputPeerChannel):
            r = await self.send(
                raw.functions.channels.GetParticipant(
                    channel=chat,
                    user_id=user
                )
            )

            users = {i.id: i for i in r.users}

            return types.ChatMember._parse(self, r.participant, users)
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user')
