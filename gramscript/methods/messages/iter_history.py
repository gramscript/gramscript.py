from gramscript.scaffold import Scaffold
from gramscript import types
from typing import Union, Optional, AsyncGenerator
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


class IterHistory(Scaffold):
    async def iter_history(
        self,
        chat_id: Union[int, str],
        limit: int = 0,
        offset: int = 0,
        offset_id: int = 0,
        offset_date: int = 0,
        reverse: bool = False
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        """Iterate through a chat history sequentially.

        This convenience method does the same as repeatedly calling :meth:`~gramscript.Client.get_history` in a loop, thus saving
        you from the hassle of setting up boilerplate code. It is useful for getting the whole chat history with a
        single call.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            limit (``int``, *optional*):
                Limits the number of messages to be retrieved.
                By default, no limit is applied and all messages are returned.

            offset (``int``, *optional*):
                Sequential number of the first message to be returned..
                Negative values are also accepted and become useful in case you set offset_id or offset_date.

            offset_id (``int``, *optional*):
                Identifier of the first message to be returned.

            offset_date (``int``, *optional*):
                Pass a date in Unix time as offset to retrieve only older messages starting from that date.

            reverse (``bool``, *optional*):
                Pass True to retrieve the messages in reversed order (from older to most recent).

        Returns:
            ``Generator``: A generator yielding :obj:`~gramscript.types.Message` objects.

        Example:
            .. code-block:: python

                for message in app.iter_history("gramscript"):
                    print(message.text)
        """
        offset_id = offset_id or (1 if reverse else 0)
        current = 0
        total = limit or (1 << 31) - 1
        limit = min(100, total)

        while True:
            messages = await self.get_history(
                chat_id=chat_id,
                limit=limit,
                offset=offset,
                offset_id=offset_id,
                offset_date=offset_date,
                reverse=reverse
            )

            if not messages:
                return

            offset_id = messages[-1].message_id + (1 if reverse else 0)

            for message in messages:
                yield message

                current += 1

                if current >= total:
                    return
