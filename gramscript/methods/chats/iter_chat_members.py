from gramscript.scaffold import Scaffold
from gramscript import types
from gramscript import raw
from typing import Union, AsyncGenerator, Optional
from string import ascii_lowercase
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


class Filters:
    ALL = "all"
    KICKED = "kicked"
    RESTRICTED = "restricted"
    BOTS = "bots"
    RECENT = "recent"
    ADMINISTRATORS = "administrators"


QUERIES = [""] + [str(i) for i in range(10)] + list(ascii_lowercase)
QUERYABLE_FILTERS = (Filters.ALL, Filters.KICKED, Filters.RESTRICTED)


class IterChatMembers(Scaffold):
    async def iter_chat_members(
        self,
        chat_id: Union[int, str],
        limit: int = 0,
        query: str = "",
        filter: str = Filters.ALL
    ) -> Optional[AsyncGenerator["types.ChatMember", None]]:
        """Iterate through the members of a chat sequentially.

        This convenience method does the same as repeatedly calling :meth:`~gramscript.Client.get_chat_members` in a loop,
        thus saving you from the hassle of setting up boilerplate code. It is useful for getting the whole members list
        of a chat with a single call.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            limit (``int``, *optional*):
                Limits the number of members to be retrieved.
                By default, no limit is applied and all members are returned.

            query (``str``, *optional*):
                Query string to filter members based on their display names and usernames.
                Defaults to "" (empty string).

            filter (``str``, *optional*):
                Filter used to select the kind of members you want to retrieve. Only applicable for supergroups
                and channels. It can be any of the followings:
                *"all"* - all kind of members,
                *"kicked"* - kicked (banned) members only,
                *"restricted"* - restricted members only,
                *"bots"* - bots only,
                *"recent"* - recent members only,
                *"administrators"* - chat administrators only.
                Defaults to *"all"*.

        Returns:
            ``Generator``: A generator yielding :obj:`~gramscript.types.ChatMember` objects.

        Example:
            .. code-block:: python

                # Iterate though all chat members
                for member in app.iter_chat_members("gramscriptchat"):
                    print(member.user.first_name)

                # Iterate though all administrators
                for member in app.iter_chat_members("gramscriptchat", filter="administrators"):
                    print(member.user.first_name)

                # Iterate though all bots
                for member in app.iter_chat_members("gramscriptchat", filter="bots"):
                    print(member.user.first_name)
        """
        current = 0
        yielded = set()
        queries = [query] if query else QUERIES
        total = limit or (1 << 31) - 1
        limit = min(200, total)
        resolved_chat_id = await self.resolve_peer(chat_id)

        if filter not in QUERYABLE_FILTERS:
            queries = [""]

        for q in queries:
            offset = 0

            while True:
                chat_members = await self.get_chat_members(
                    chat_id=chat_id,
                    offset=offset,
                    limit=limit,
                    query=q,
                    filter=filter
                )

                if not chat_members:
                    break

                if isinstance(resolved_chat_id, raw.types.InputPeerChat):
                    total = len(chat_members)

                offset += len(chat_members)

                for chat_member in chat_members:
                    user_id = chat_member.user.id

                    if user_id in yielded:
                        continue

                    yield chat_member

                    yielded.add(chat_member.user.id)

                    current += 1

                    if current >= total:
                        return
