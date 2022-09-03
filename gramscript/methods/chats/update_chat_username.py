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


class UpdateChatUsername(Scaffold):
    async def update_chat_username(
        self,
        chat_id: Union[int, str],
        username: Union[str, None]
    ) -> bool:
        """Update a channel or a supergroup username.

        To update your own username (for users only, not bots) you can use :meth:`~gramscript.Client.update_username`.

        Parameters:
            chat_id (``int`` | ``str``)
                Unique identifier (int) or username (str) of the target chat.
            username (``str`` | ``None``):
                Username to set. Pass "" (empty string) or None to remove the username.

        Returns:
            ``bool``: True on success.

        Raises:
            ValueError: In case a chat id belongs to a user or chat.

        Example:
            .. code-block:: python

                app.update_chat_username(chat_id, "new_username")
        """

        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            return bool(
                await self.send(
                    raw.functions.channels.UpdateUsername(
                        channel=peer,
                        username=username or ""
                    )
                )
            )
        else:
            raise ValueError(
                f'The chat_id "{chat_id}" belongs to a user or chat')
