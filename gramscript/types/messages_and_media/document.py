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


class Document(Object):
    """A generic file (as opposed to photos, voice messages, audio files, ...).

    Parameters:
        file_id (``str``):
            Unique file identifier.

        file_ref (``str``):
            Up to date file reference.

        file_name (``str``, *optional*):
            Original filename as defined by sender.

        mime_type (``str``, *optional*):
            MIME type of the file as defined by sender.

        file_size (``int``, *optional*):
            File size.

        date (``int``, *optional*):
            Date the document was sent in Unix time.

        thumbs (List of :obj:`~gramscript.types.Thumbnail`, *optional*):
            Document thumbnails as defined by sender.
    """

    def __init__(
        self,
        *,
        client: "gramscript.Client" = None,
        file_id: str,
        file_ref: str,
        file_name: str = None,
        mime_type: str = None,
        file_size: int = None,
        date: int = None,
        thumbs: List["types.Thumbnail"] = None
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_ref = file_ref
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date
        self.thumbs = thumbs

    @staticmethod
    def _parse(client, document: "raw.types.Document", file_name: str) -> "Document":
        return Document(
            file_id=encode_file_id(
                pack(
                    "<iiqq",
                    5,
                    document.dc_id,
                    document.id,
                    document.access_hash
                )
            ),
            file_ref=encode_file_ref(document.file_reference),
            file_name=file_name,
            mime_type=document.mime_type,
            file_size=document.size,
            date=document.date,
            thumbs=types.Thumbnail._parse(client, document),
            client=client
        )
