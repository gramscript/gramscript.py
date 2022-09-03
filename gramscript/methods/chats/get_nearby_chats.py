from gramscript.scaffold import Scaffold
from gramscript import utils
from gramscript import types
from gramscript import raw
from typing import List
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


class GetNearbyChats(Scaffold):
    async def get_nearby_chats(
        self,
        latitude: float,
        longitude: float
    ) -> List["types.Chat"]:
        """Get nearby chats.

        Parameters:
            latitude (``float``):
                Latitude of the location.

            longitude (``float``):
                Longitude of the location.

        Returns:
            List of :obj:`~gramscript.types.Chat`: On success, a list of nearby chats is returned.

        Example:
            .. code-block:: python

                chats = app.get_nearby_chats(51.500729, -0.124583)
                print(chats)
        """

        r = await self.send(
            raw.functions.contacts.GetLocated(
                geo_point=raw.types.InputGeoPoint(
                    lat=latitude,
                    long=longitude
                )
            )
        )

        if not r.updates:
            return []

        chats = types.List([types.Chat._parse_chat(self, chat)
                           for chat in r.chats])
        peers = r.updates[0].peers

        for peer in peers:
            if isinstance(peer.peer, raw.types.PeerChannel):
                chat_id = utils.get_channel_id(peer.peer.channel_id)

                for chat in chats:
                    if chat.id == chat_id:
                        chat.distance = peer.distance
                        break

        return chats
