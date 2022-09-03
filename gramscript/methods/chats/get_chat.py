from gramscript.scaffold import Scaffold
from gramscript import utils
from gramscript import types
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


class GetChat(Scaffold):
    async def get_chat(
        self,
        chat_id: Union[int, str]
    ) -> Union["types.Chat", "types.ChatPreview"]:
        """Get up to date information about a chat.

        Information include current name of the user for one-on-one conversations, current username of a user, group or
        channel, etc.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                Unique identifier for the target chat in form of a *t.me/joinchat/* link, identifier (int) or username
                of the target channel/supergroup (in the format @username).

        Returns:
            :obj:`~gramscript.types.Chat` | :obj:`~gramscript.types.ChatPreview`: On success, if you've already joined the chat, a chat object is returned,
            otherwise, a chat preview object is returned.

        Raises:
            ValueError: In case the chat invite link points to a chat you haven't joined yet.

        Example:
            .. code-block:: python

                chat = app.get_chat("gramscript")
                print(chat)
        """
        match = self.INVITE_LINK_RE.match(str(chat_id))

        if match:
            r = await self.send(
                raw.functions.messages.CheckChatInvite(
                    hash=match.group(1)
                )
            )

            if isinstance(r, raw.types.ChatInvite):
                return types.ChatPreview._parse(self, r)

            await self.fetch_peers([r.chat])

            if isinstance(r.chat, types.Chat):
                chat_id = -r.chat.id

            if isinstance(r.chat, raw.types.Channel):
                chat_id = utils.get_channel_id(r.chat.id)

        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            r = await self.send(raw.functions.channels.GetFullChannel(channel=peer))
        elif isinstance(peer, (raw.types.InputPeerUser, raw.types.InputPeerSelf)):
            r = await self.send(raw.functions.users.GetFullUser(id=peer))
        else:
            r = await self.send(raw.functions.messages.GetFullChat(chat_id=peer.chat_id))

        return await types.Chat._parse_full(self, r)
