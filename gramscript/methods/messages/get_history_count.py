from gramscript.scaffold import Scaffold
from gramscript import raw
from typing import Union
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


log = logging.getLogger(__name__)


class GetHistoryCount(Scaffold):
    async def get_history_count(
        self,
        chat_id: Union[int, str]
    ) -> int:
        """Get the total count of messages in a chat.

        .. note::

            Due to Telegram latest internal changes, the server can't reliably find anymore the total count of messages
            a **private** or a **basic group** chat has with a single method call. To overcome this limitation, gramscript
            has to iterate over all the messages. Channels and supergroups are not affected by this limitation.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

        Returns:
            ``int``: On success, the chat history count is returned.

        Example:
            .. code-block:: python

                app.get_history_count("gramscriptchat")
        """

        r = await self.send(
            raw.functions.messages.GetHistory(
                peer=await self.resolve_peer(chat_id),
                offset_id=0,
                offset_date=0,
                add_offset=0,
                limit=1,
                max_id=0,
                min_id=0,
                hash=0
            )
        )

        if isinstance(r, raw.types.messages.Messages):
            return len(r.messages)
        else:
            return r.count
