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


class UnpinChatMessage(Scaffold):
    async def unpin_chat_message(
        self,
        chat_id: Union[int, str]
    ) -> bool:
        """Unpin a message in a group, channel or your own chat.
        You must be an administrator in the chat for this to work and must have the "can_pin_messages" admin
        right in the supergroup or "can_edit_messages" admin right in the channel.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                app.unpin_chat_message(chat_id)
        """
        await self.send(
            raw.functions.messages.UpdatePinnedMessage(
                peer=await self.resolve_peer(chat_id),
                id=0
            )
        )

        return True
