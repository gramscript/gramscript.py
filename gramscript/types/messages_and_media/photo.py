from ..object import Object
from gramscript.utils import encode_file_id, encode_file_ref
from gramscript import types
from gramscript import raw
import gramscript
from typing import List
from struct import pack
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


class Photo(Object):
    """A Photo.

    Parameters:
        file_id (``str``):
            Unique identifier for this photo.

        file_ref (``str``):
            Up to date file reference.

        width (``int``):
            Photo width.

        height (``int``):
            Photo height.

        file_size (``int``):
            File size.

        date (``int``):
            Date the photo was sent in Unix time.

        ttl_seconds (``int``, *optional*):
            Time-to-live seconds, for secret photos.

        thumbs (List of :obj:`~gramscript.types.Thumbnail`, *optional*):
            Available thumbnails of this photo.
    """

    def __init__(
        self,
        *,
        client: "gramscript.Client" = None,
        file_id: str,
        file_ref: str,
        width: int,
        height: int,
        file_size: int,
        date: int,
        ttl_seconds: int = None,
        thumbs: List["types.Thumbnail"] = None
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_ref = file_ref
        self.width = width
        self.height = height
        self.file_size = file_size
        self.date = date
        self.ttl_seconds = ttl_seconds
        self.thumbs = thumbs

    @staticmethod
    def _parse(client, photo: "raw.types.Photo", ttl_seconds: int = None) -> "Photo":
        if isinstance(photo, raw.types.Photo):
            big = list(filter(lambda p: isinstance(
                p, raw.types.PhotoSize), photo.sizes))[-1]

            return Photo(
                file_id=encode_file_id(
                    pack(
                        "<iiqqqiiii",
                        2, photo.dc_id, photo.id, photo.access_hash,
                        big.location.volume_id, 1, 2, ord(big.type),
                        big.location.local_id
                    )
                ),
                file_ref=encode_file_ref(photo.file_reference),
                width=big.w,
                height=big.h,
                file_size=big.size,
                date=photo.date,
                ttl_seconds=ttl_seconds,
                thumbs=types.Thumbnail._parse(client, photo),
                client=client
            )
