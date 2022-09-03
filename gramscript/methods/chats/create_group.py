from gramscript.scaffold import Scaffold
from gramscript import types
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


class CreateGroup(Scaffold):
    async def create_group(
        self,
        title: str,
        users: Union[Union[int, str], List[Union[int, str]]]
    ) -> "types.Chat":
        """Create a new basic group.

        .. note::

            If you want to create a new supergroup, use :meth:`~gramscript.Client.create_supergroup` instead.

        Parameters:
            title (``str``):
                The group title.

            users (``int`` | ``str`` | List of ``int`` or ``str``):
                Users to create a chat with.
                You must pass at least one user using their IDs (int), usernames (str) or phone numbers (str).
                Multiple users can be invited by passing a list of IDs, usernames or phone numbers.

        Returns:
            :obj:`~gramscript.types.Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                app.create_group("Group Title", user_id)
        """
        if not isinstance(users, list):
            users = [users]

        r = await self.send(
            raw.functions.messages.CreateChat(
                title=title,
                users=[await self.resolve_peer(u) for u in users]
            )
        )

        return types.Chat._parse_chat(self, r.chats[0])
