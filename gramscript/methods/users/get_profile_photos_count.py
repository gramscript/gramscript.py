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


class GetProfilePhotosCount(Scaffold):
    async def get_profile_photos_count(self, chat_id: Union[int, str]) -> int:
        """Get the total count of profile pictures for a user.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

        Returns:
            ``int``: On success, the user profile photos count is returned.

        Example:
            .. code-block:: python

                count = app.get_profile_photos_count("haskell")
                print(count)
        """

        peer_id = await self.resolve_peer(chat_id)

        if isinstance(peer_id, raw.types.InputPeerChannel):
            r = await self.send(
                raw.functions.messages.GetSearchCounters(
                    peer=peer_id,
                    filters=[raw.types.InputMessagesFilterChatPhotos()],
                )
            )

            return r[0].count
        else:
            r = await self.send(
                raw.functions.photos.GetUserPhotos(
                    user_id=peer_id,
                    offset=0,
                    max_id=0,
                    limit=1
                )
            )

            if isinstance(r, raw.types.photos.Photos):
                return len(r.photos)
            else:
                return r.count
