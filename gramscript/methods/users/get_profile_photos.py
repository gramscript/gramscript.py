from gramscript.scaffold import Scaffold
from gramscript import utils
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


class GetProfilePhotos(Scaffold):
    async def get_profile_photos(
        self,
        chat_id: Union[int, str],
        offset: int = 0,
        limit: int = 100
    ) -> List["types.Photo"]:
        """Get a list of profile pictures for a user or a chat.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            offset (``int``, *optional*):
                Sequential number of the first photo to be returned.
                By default, all photos are returned.

            limit (``int``, *optional*):
                Limits the number of photos to be retrieved.
                Values between 1—100 are accepted. Defaults to 100.

        Returns:
            List of :obj:`~gramscript.types.Photo`: On success, a list of profile photos is returned.

        Example:
            .. code-block:: python

                # Get the first 100 profile photos of a user
                app.get_profile_photos("haskell")

                # Get only the first profile photo of a user
                app.get_profile_photos("haskell", limit=1)

                # Get 3 profile photos of a user, skip the first 5
                app.get_profile_photos("haskell", limit=3, offset=5)
        """
        peer_id = await self.resolve_peer(chat_id)

        if isinstance(peer_id, raw.types.InputPeerChannel):
            r = await utils.parse_messages(
                self,
                await self.send(
                    raw.functions.messages.Search(
                        peer=peer_id,
                        q="",
                        filter=raw.types.InputMessagesFilterChatPhotos(),
                        min_date=0,
                        max_date=0,
                        offset_id=0,
                        add_offset=offset,
                        limit=limit,
                        max_id=0,
                        min_id=0,
                        hash=0
                    )
                )
            )

            return types.List([message.new_chat_photo for message in r][:limit])
        else:
            r = await self.send(
                raw.functions.photos.GetUserPhotos(
                    user_id=peer_id,
                    offset=offset,
                    max_id=0,
                    limit=limit
                )
            )

            return types.List(types.Photo._parse(self, photo) for photo in r.photos)
