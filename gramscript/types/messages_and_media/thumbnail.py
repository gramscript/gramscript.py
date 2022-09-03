from ..object import Object
from gramscript.utils import encode_file_id
from gramscript import types
from gramscript import raw
import gramscript
from typing import Union, List
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


class Thumbnail(Object):
    """One size of a photo or a file/sticker thumbnail.

    Parameters:
        file_id (``str``):
            Unique identifier for this file.

        width (``int``):
            Photo width.

        height (``int``):
            Photo height.

        file_size (``int``):
            File size.
    """

    def __init__(
        self,
        *,
        client: "gramscript.Client" = None,
        file_id: str,
        width: int,
        height: int,
        file_size: int
    ):
        super().__init__(client)

        self.file_id = file_id
        self.width = width
        self.height = height
        self.file_size = file_size

    @staticmethod
    def _parse(
        client,
        media: Union["raw.types.Photo", "raw.types.Document"]
    ) -> Union[List[Union["types.StrippedThumbnail", "Thumbnail"]], None]:
        if isinstance(media, raw.types.Photo):
            raw_thumbnails = media.sizes[:-1]
            media_type = 2
        elif isinstance(media, raw.types.Document):
            raw_thumbnails = media.thumbs
            media_type = 14

            if not raw_thumbnails:
                return None
        else:
            return None

        thumbnails = []

        for thumbnail in raw_thumbnails:
            # TODO: Enable this
            # if isinstance(thumbnail, types.PhotoStrippedSize):
            #     thumbnails.append(StrippedThumbnail._parse(client, thumbnail))
            if isinstance(thumbnail, raw.types.PhotoSize):
                thumbnails.append(
                    Thumbnail(
                        file_id=encode_file_id(
                            pack(
                                "<iiqqqiiii",
                                media_type, media.dc_id, media.id, media.access_hash,
                                thumbnail.location.volume_id, 1, 2, ord(
                                    thumbnail.type),
                                thumbnail.location.local_id
                            )
                        ),
                        width=thumbnail.w,
                        height=thumbnail.h,
                        file_size=thumbnail.size,
                        client=client
                    )
                )

        return thumbnails or None
