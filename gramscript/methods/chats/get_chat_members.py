from gramscript.scaffold import Scaffold
from gramscript import types
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


log = logging.getLogger(__name__)


class Filters:
    ALL = "all"
    KICKED = "kicked"
    RESTRICTED = "restricted"
    BOTS = "bots"
    RECENT = "recent"
    ADMINISTRATORS = "administrators"


class GetChatMembers(Scaffold):
    async def get_chat_members(
        self,
        chat_id: Union[int, str],
        offset: int = 0,
        limit: int = 200,
        query: str = "",
        filter: str = Filters.ALL
    ) -> List["types.ChatMember"]:
        """Get a chunk of the members list of a chat.

        You can get up to 200 chat members at once.
        A chat can be either a basic group, a supergroup or a channel.
        You must be admin to retrieve the members list of a channel (also known as "subscribers").
        For a more convenient way of getting chat members see :meth:`~gramscript.Client.iter_chat_members`.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            offset (``int``, *optional*):
                Sequential number of the first member to be returned.
                Only applicable to supergroups and channels. Defaults to 0 [1]_.

            limit (``int``, *optional*):
                Limits the number of members to be retrieved.
                Only applicable to supergroups and channels.
                Defaults to 200, which is also the maximum server limit allowed per method call.

            query (``str``, *optional*):
                Query string to filter members based on their display names and usernames.
                Only applicable to supergroups and channels. Defaults to "" (empty string) [2]_.

            filter (``str``, *optional*):
                Filter used to select the kind of members you want to retrieve. Only applicable for supergroups
                and channels. It can be any of the followings:
                *"all"* - all kind of members,
                *"kicked"* - kicked (banned) members only,
                *"restricted"* - restricted members only,
                *"bots"* - bots only,
                *"recent"* - recent members only,
                *"administrators"* - chat administrators only.
                Only applicable to supergroups and channels.
                Defaults to *"all"*.

        .. [1] Server limit: on supergroups, you can get up to 10,000 members for a single query and up to 200 members
            on channels.

        .. [2] A query string is applicable only for *"all"*, *"kicked"* and *"restricted"* filters only.

        Returns:
            List of :obj:`~gramscript.types.ChatMember`: On success, a list of chat members is returned.

        Raises:
            ValueError: In case you used an invalid filter or a chat id that belongs to a user.

        Example:
            .. code-block:: python

                # Get first 200 recent members
                app.get_chat_members("gramscriptchat")

                # Get all administrators
                app.get_chat_members("gramscriptchat", filter="administrators")

                # Get all bots
                app.get_chat_members("gramscriptchat", filter="bots")
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChat):
            r = await self.send(
                raw.functions.messages.GetFullChat(
                    chat_id=peer.chat_id
                )
            )

            members = r.full_chat.participants.participants
            users = {i.id: i for i in r.users}

            return types.List(types.ChatMember._parse(self, member, users) for member in members)
        elif isinstance(peer, raw.types.InputPeerChannel):
            filter = filter.lower()

            if filter == Filters.ALL:
                filter = raw.types.ChannelParticipantsSearch(q=query)
            elif filter == Filters.KICKED:
                filter = raw.types.ChannelParticipantsKicked(q=query)
            elif filter == Filters.RESTRICTED:
                filter = raw.types.ChannelParticipantsBanned(q=query)
            elif filter == Filters.BOTS:
                filter = raw.types.ChannelParticipantsBots()
            elif filter == Filters.RECENT:
                filter = raw.types.ChannelParticipantsRecent()
            elif filter == Filters.ADMINISTRATORS:
                filter = raw.types.ChannelParticipantsAdmins()
            else:
                raise ValueError(f'Invalid filter "{filter}"')

            r = await self.send(
                raw.functions.channels.GetParticipants(
                    channel=peer,
                    filter=filter,
                    offset=offset,
                    limit=limit,
                    hash=0
                )
            )

            members = r.participants
            users = {i.id: i for i in r.users}

            return types.List(types.ChatMember._parse(self, member, users) for member in members)
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user')
