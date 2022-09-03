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


class LeaveChat(Scaffold):
    async def leave_chat(
        self,
        chat_id: Union[int, str],
        delete: bool = False
    ):
        """Leave a group chat or channel.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).

            delete (``bool``, *optional*):
                Deletes the group chat dialog after leaving (for simple group chats, not supergroups).
                Defaults to False.

        Example:
            .. code-block:: python

                # Leave chat or channel
                app.leave_chat(chat_id)

                # Leave basic chat and also delete the dialog
                app.leave_chat(chat_id, delete=True)
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            return await self.send(
                raw.functions.channels.LeaveChannel(
                    channel=await self.resolve_peer(chat_id)
                )
            )
        elif isinstance(peer, raw.types.InputPeerChat):
            r = await self.send(
                raw.functions.messages.DeleteChatUser(
                    chat_id=peer.chat_id,
                    user_id=raw.types.InputUserSelf()
                )
            )

            if delete:
                await self.send(
                    raw.functions.messages.DeleteHistory(
                        peer=peer,
                        max_id=0
                    )
                )

            return r
