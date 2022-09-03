from gramscript.scaffold import Scaffold
from gramscript import types
from typing import Union, AsyncGenerator, Optional
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


class IterProfilePhotos(Scaffold):
    async def iter_profile_photos(
        self,
        chat_id: Union[int, str],
        offset: int = 0,
        limit: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        """Iterate through a chat or a user profile photos sequentially.

        This convenience method does the same as repeatedly calling :meth:`~gramscript.Client.get_profile_photos` in a
        loop, thus saving you from the hassle of setting up boilerplate code. It is useful for getting all the profile
        photos with a single call.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            limit (``int``, *optional*):
                Limits the number of profile photos to be retrieved.
                By default, no limit is applied and all profile photos are returned.

            offset (``int``, *optional*):
                Sequential number of the first profile photo to be returned.

        Returns:
            ``Generator``: A generator yielding :obj:`~gramscript.types.Photo` objects.

        Example:
            .. code-block:: python

                for photo in app.iter_profile_photos("haskell"):
                    print(photo.file_id)
        """
        current = 0
        total = limit or (1 << 31)
        limit = min(100, total)

        while True:
            photos = await self.get_profile_photos(
                chat_id=chat_id,
                offset=offset,
                limit=limit
            )

            if not photos:
                return

            offset += len(photos)

            for photo in photos:
                yield photo

                current += 1

                if current >= total:
                    return
