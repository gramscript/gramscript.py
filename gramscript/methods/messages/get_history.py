from gramscript.scaffold import Scaffold
from gramscript import utils
from gramscript import raw
from typing import Union, List
import logging
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


# from gramscript import types

log = logging.getLogger(__name__)


class GetHistory(Scaffold):
    async def get_history(
        self,
        chat_id: Union[int, str],
        limit: int = 100,
        offset: int = 0,
        offset_id: int = 0,
        offset_date: int = 0,
        reverse: bool = False
    ) -> List["types.Message"]:
        """Retrieve a chunk of the history of a chat.

        You can get up to 100 messages at once.
        For a more convenient way of getting a chat history see :meth:`~gramscript.Client.iter_history`.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            limit (``int``, *optional*):
                Limits the number of messages to be retrieved.
                By default, the first 100 messages are returned.

            offset (``int``, *optional*):
                Sequential number of the first message to be returned. Defaults to 0 (most recent message).
                Negative values are also accepted and become useful in case you set offset_id or offset_date.

            offset_id (``int``, *optional*):
                Pass a message identifier as offset to retrieve only older messages starting from that message.

            offset_date (``int``, *optional*):
                Pass a date in Unix time as offset to retrieve only older messages starting from that date.

            reverse (``bool``, *optional*):
                Pass True to retrieve the messages in reversed order (from older to most recent).

        Returns:
            List of :obj:`~gramscript.types.Message` - On success, a list of the retrieved messages is returned.

        Example:
            .. code-block:: python

                # Get the last 100 messages of a chat
                app.get_history("gramscriptchat")

                # Get the last 3 messages of a chat
                app.get_history("gramscriptchat", limit=3)

                # Get 3 messages after skipping the first 5
                app.get_history("gramscriptchat", offset=5, limit=3)
        """

        offset_id = offset_id or (1 if reverse else 0)

        messages = await utils.parse_messages(
            self,
            await self.send(
                raw.functions.messages.GetHistory(
                    peer=await self.resolve_peer(chat_id),
                    offset_id=offset_id,
                    offset_date=offset_date,
                    add_offset=offset * (-1 if reverse else 1) -
                    (limit if reverse else 0),
                    limit=limit,
                    max_id=0,
                    min_id=0,
                    hash=0
                )
            )
        )

        if reverse:
            messages.reverse()

        return messages
