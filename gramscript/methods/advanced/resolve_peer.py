from gramscript.scaffold import Scaffold
from gramscript.errors import PeerIdInvalid
from gramscript import utils
from gramscript import raw
from typing import Union
import re
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


class ResolvePeer(Scaffold):
    async def resolve_peer(
        self,
        peer_id: Union[int, str]
    ) -> Union[raw.base.InputPeer, raw.base.InputUser, raw.base.InputChannel]:
        """Get the InputPeer of a known peer id.
        Useful whenever an InputPeer type is required.

        .. note::

            This is a utility method intended to be used **only** when working with raw
            :obj:`functions <gramscript.api.functions>` (i.e: a Telegram API method you wish to use which is not
            available yet in the Client class as an easy-to-use method).

        Parameters:
            peer_id (``int`` | ``str``):
                The peer id you want to extract the InputPeer from.
                Can be a direct id (int), a username (str) or a phone number (str).

        Returns:
            ``InputPeer``: On success, the resolved peer id is returned in form of an InputPeer object.

        Raises:
            KeyError: In case the peer doesn't exist in the internal database.
        """
        if not self.is_connected:
            raise ConnectionError("Client has not been started yet")

        try:
            return await self.storage.get_peer_by_id(peer_id)
        except KeyError:
            if isinstance(peer_id, str):
                if peer_id in ("self", "me"):
                    return raw.types.InputPeerSelf()

                peer_id = re.sub(r"[@+\s]", "", peer_id.lower())

                try:
                    int(peer_id)
                except ValueError:
                    try:
                        return await self.storage.get_peer_by_username(peer_id)
                    except KeyError:
                        await self.send(
                            raw.functions.contacts.ResolveUsername(
                                username=peer_id
                            )
                        )

                        return await self.storage.get_peer_by_username(peer_id)
                else:
                    try:
                        return await self.storage.get_peer_by_phone_number(peer_id)
                    except KeyError:
                        raise PeerIdInvalid

            peer_type = utils.get_peer_type(peer_id)

            if peer_type == "user":
                await self.fetch_peers(
                    await self.send(
                        raw.functions.users.GetUsers(
                            id=[
                                raw.types.InputUser(
                                    user_id=peer_id,
                                    access_hash=0
                                )
                            ]
                        )
                    )
                )
            elif peer_type == "chat":
                await self.send(
                    raw.functions.messages.GetChats(
                        id=[-peer_id]
                    )
                )
            else:
                await self.send(
                    raw.functions.channels.GetChannels(
                        id=[
                            raw.types.InputChannel(
                                channel_id=utils.get_channel_id(peer_id),
                                access_hash=0
                            )
                        ]
                    )
                )

            try:
                return await self.storage.get_peer_by_id(peer_id)
            except KeyError:
                raise PeerIdInvalid
