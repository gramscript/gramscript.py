from gramscript.scaffold import Scaffold
from gramscript import utils
from gramscript import types
from gramscript import raw
from typing import AsyncGenerator, Optional
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


class SearchGlobal(Scaffold):
    async def search_global(
        self,
        query: str,
        limit: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        """Search messages globally from all of your chats.

        .. note::

            Due to server-side limitations, you can only get up to around ~10,000 messages and each message
            retrieved will not have any *reply_to_message* field.

        Parameters:
            query (``str``):
                Text query string.

            limit (``int``, *optional*):
                Limits the number of messages to be retrieved.
                By default, no limit is applied and all messages are returned.

        Returns:
            ``Generator``: A generator yielding :obj:`~gramscript.types.Message` objects.

        Example:
            .. code-block:: python

                # Search for "gramscript". Get the first 420 results
                for message in app.search_global("gramscript", limit=420):
                    print(message.text)
        """
        current = 0
        # There seems to be an hard limit of 10k, beyond which Telegram starts spitting one message at a time.
        total = abs(limit) or (1 << 31)
        limit = min(100, total)

        offset_date = 0
        offset_peer = raw.types.InputPeerEmpty()
        offset_id = 0

        while True:
            messages = await utils.parse_messages(
                self,
                await self.send(
                    raw.functions.messages.SearchGlobal(
                        q=query,
                        offset_rate=offset_date,
                        offset_peer=offset_peer,
                        offset_id=offset_id,
                        limit=limit
                    )
                ),
                replies=0
            )

            if not messages:
                return

            last = messages[-1]

            offset_date = last.date
            offset_peer = await self.resolve_peer(last.chat.id)
            offset_id = last.message_id

            for message in messages:
                yield message

                current += 1

                if current >= total:
                    return
