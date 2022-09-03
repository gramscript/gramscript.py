from gramscript.scaffold import Scaffold
from gramscript import types
from gramscript import raw
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


class CreateChannel(Scaffold):
    async def create_channel(
        self,
        title: str,
        description: str = ""
    ) -> "types.Chat":
        """Create a new broadcast channel.

        Parameters:
            title (``str``):
                The channel title.

            description (``str``, *optional*):
                The channel description.

        Returns:
            :obj:`~gramscript.types.Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                app.create_channel("Channel Title", "Channel Description")
        """
        r = await self.send(
            raw.functions.channels.CreateChannel(
                title=title,
                about=description,
                broadcast=True
            )
        )

        return types.Chat._parse_chat(self, r.chats[0])
