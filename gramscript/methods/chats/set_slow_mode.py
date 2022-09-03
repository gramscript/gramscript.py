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


class SetSlowMode(Scaffold):
    async def set_slow_mode(
        self,
        chat_id: Union[int, str],
        seconds: Union[int, None]
    ) -> bool:
        """Set the slow mode interval for a chat.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            seconds (``int`` | ``None``):
                Seconds in which members will be able to send only one message per this interval.
                Valid values are: 0 or None (off), 10, 30, 60 (1m), 300 (5m), 900 (15m) or 3600 (1h).

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Set slow mode to 60 seconds
                app.set_slow_mode("gramscriptchat", 60)

                # Disable slow mode
                app.set_slow_mode("gramscriptchat", None)
        """

        await self.send(
            raw.functions.channels.ToggleSlowMode(
                channel=await self.resolve_peer(chat_id),
                seconds=0 if seconds is None else seconds
            )
        )

        return True
