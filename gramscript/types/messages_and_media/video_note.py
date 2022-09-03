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


class VideoNote(Object):
    """A video note.

    Parameters:
        file_id (``str``):
            Unique identifier for this file.

        file_ref (``str``):
            Up to date file reference.

        length (``int``):
            Video width and height as defined by sender.

        duration (``int``):
            Duration of the video in seconds as defined by sender.

        mime_type (``str``, *optional*):
            MIME type of the file as defined by sender.

        file_size (``int``, *optional*):
            File size.

        date (``int``, *optional*):
            Date the video note was sent in Unix time.

        thumbs (List of :obj:`~gramscript.types.Thumbnail`, *optional*):
            Video thumbnails.
    """

    def __init__(
        self,
        *,
        client: "gramscript.Client" = None,
        file_id: str,
        file_ref: str,
        length: int,
        duration: int,
        thumbs: List["types.Thumbnail"] = None,
        mime_type: str = None,
        file_size: int = None,
        date: int = None
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_ref = file_ref
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date
        self.length = length
        self.duration = duration
        self.thumbs = thumbs

    @staticmethod
    def _parse(
        client,
        video_note: "raw.types.Document",
        video_attributes: "raw.types.DocumentAttributeVideo"
    ) -> "VideoNote":
        return VideoNote(
            file_id=encode_file_id(
                pack(
                    "<iiqq",
                    13,
                    video_note.dc_id,
                    video_note.id,
                    video_note.access_hash
                )
            ),
            file_ref=encode_file_ref(video_note.file_reference),
            length=video_attributes.w,
            duration=video_attributes.duration,
            file_size=video_note.size,
            mime_type=video_note.mime_type,
            date=video_note.date,
            thumbs=types.Thumbnail._parse(client, video_note),
            client=client
        )
