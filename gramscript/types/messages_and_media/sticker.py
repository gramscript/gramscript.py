from ..object import Object
from gramscript.utils import encode_file_id, encode_file_ref
from gramscript.errors import StickersetInvalid
from gramscript import types
from gramscript import raw
import gramscript
from async_lru import alru_cache
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


class Sticker(Object):
    """A sticker.

    Parameters:
        file_id (``str``):
            Unique identifier for this file.

        file_ref (``str``):
            Up to date file reference.

        width (``int``):
            Sticker width.

        height (``int``):
            Sticker height.

        is_animated (``bool``):
            True, if the sticker is animated

        file_name (``str``, *optional*):
            Sticker file name.

        mime_type (``str``, *optional*):
            MIME type of the file as defined by sender.

        file_size (``int``, *optional*):
            File size.

        date (``int``, *optional*):
            Date the sticker was sent in Unix time.

        emoji (``str``, *optional*):
            Emoji associated with the sticker.

        set_name (``str``, *optional*):
            Name of the sticker set to which the sticker belongs.

        thumbs (List of :obj:`~gramscript.types.Thumbnail`, *optional*):
            Sticker thumbnails in the .webp or .jpg format.
    """

    # TODO: Add mask position

    def __init__(
        self,
        *,
        client: "gramscript.Client" = None,
        file_id: str,
        file_ref: str,
        width: int,
        height: int,
        is_animated: bool,
        file_name: str = None,
        mime_type: str = None,
        file_size: int = None,
        date: int = None,
        emoji: str = None,
        set_name: str = None,
        thumbs: List["types.Thumbnail"] = None
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_ref = file_ref
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date
        self.width = width
        self.height = height
        self.is_animated = is_animated
        self.emoji = emoji
        self.set_name = set_name
        self.thumbs = thumbs
        # self.mask_position = mask_position

    @staticmethod
    @alru_cache(maxsize=256)
    async def _get_sticker_set_name(send, input_sticker_set_id):
        try:
            return (await send(
                raw.functions.messages.GetStickerSet(
                    stickerset=raw.types.InputStickerSetID(
                        id=input_sticker_set_id[0],
                        access_hash=input_sticker_set_id[1]
                    )
                )
            )).set.short_name
        except StickersetInvalid:
            return None

    @staticmethod
    async def _parse(
        client,
        sticker: "raw.types.Document",
        image_size_attributes: "raw.types.DocumentAttributeImageSize",
        sticker_attributes: "raw.types.DocumentAttributeSticker",
        file_name: str
    ) -> "Sticker":
        sticker_set = sticker_attributes.stickerset

        if isinstance(sticker_set, raw.types.InputStickerSetID):
            input_sticker_set_id = (sticker_set.id, sticker_set.access_hash)
            set_name = await Sticker._get_sticker_set_name(client.send, input_sticker_set_id)
        else:
            set_name = None

        return Sticker(
            file_id=encode_file_id(
                pack(
                    "<iiqq",
                    8,
                    sticker.dc_id,
                    sticker.id,
                    sticker.access_hash
                )
            ),
            file_ref=encode_file_ref(sticker.file_reference),
            width=image_size_attributes.w if image_size_attributes else 512,
            height=image_size_attributes.h if image_size_attributes else 512,
            is_animated=sticker.mime_type == "application/x-tgsticker",
            # TODO: mask_position
            set_name=set_name,
            emoji=sticker_attributes.alt or None,
            file_size=sticker.size,
            mime_type=sticker.mime_type,
            file_name=file_name,
            date=sticker.date,
            thumbs=types.Thumbnail._parse(client, sticker),
            client=client
        )
