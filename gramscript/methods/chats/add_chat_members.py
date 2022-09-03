from gramscript.scaffold import Scaffold
from gramscript import raw
from typing import Union, List
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


class AddChatMembers(Scaffold):
    async def add_chat_members(
        self,
        chat_id: Union[int, str],
        user_ids: Union[Union[int, str], List[Union[int, str]]],
        forward_limit: int = 100
    ) -> bool:
        """Add new chat members to a group, supergroup or channel

        Parameters:
            chat_id (``int`` | ``str``):
                The group, supergroup or channel id

            user_ids (``int`` | ``str`` | List of ``int`` or ``str``):
                Users to add in the chat
                You can pass an ID (int), username (str) or phone number (str).
                Multiple users can be added by passing a list of IDs, usernames or phone numbers.

            forward_limit (``int``, *optional*):
                How many of the latest messages you want to forward to the new members. Pass 0 to forward none of them.
                Only applicable to basic groups (the argument is ignored for supergroups or channels).
                Defaults to 100 (max amount).

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Add one member to a group or channel
                app.add_chat_members(chat_id, user_id)

                # Add multiple members to a group or channel
                app.add_chat_members(chat_id, [user_id1, user_id2, user_id3])

                # Change forward_limit (for basic groups only)
                app.add_chat_members(chat_id, user_id, forward_limit=25)
        """
        peer = await self.resolve_peer(chat_id)

        if not isinstance(user_ids, list):
            user_ids = [user_ids]

        if isinstance(peer, raw.types.InputPeerChat):
            for user_id in user_ids:
                await self.send(
                    raw.functions.messages.AddChatUser(
                        chat_id=peer.chat_id,
                        user_id=await self.resolve_peer(user_id),
                        fwd_limit=forward_limit
                    )
                )
        else:
            await self.send(
                raw.functions.channels.InviteToChannel(
                    channel=peer,
                    users=[
                        await self.resolve_peer(user_id)
                        for user_id in user_ids
                    ]
                )
            )

        return True
