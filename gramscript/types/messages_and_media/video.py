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


class Video(Object):
    """A video file.

    Parameters:
        file_id (``str``):
            Unique identifier for this file.

        file_ref (``str``):
            Up to date file reference.

        width (``int``):
            Video width as defined by sender.

        height (``int``):
            Video height as defined by sender.

        duration (``int``):
            Duration of the video in seconds as defined by sender.

        file_name (``str``, *optional*):
            Video file name.

        mime_type (``str``, *optional*):
            Mime type of a file as defined by sender.

        supports_streaming (``bool``, *optional*):
            True, if the video was uploaded with streaming support.

        file_size (``int``, *optional*):
            File size.

        date (``int``, *optional*):
            Date the video was sent in Unix time.

        ttl_seconds (``int``. *optional*):
            Time-to-live seconds, for secret photos.

        thumbs (List of :obj:`~gramscript.types.Thumbnail`, *optional*):
            Video thumbnails.
    """

    def __init__(
        self,
        *,
        client: "gramscript.Client" = None,
        file_id: str,
        file_ref: str,
        width: int,
        height: int,
        duration: int,
        file_name: str = None,
        mime_type: str = None,
        supports_streaming: bool = None,
        file_size: int = None,
        date: int = None,
        ttl_seconds: int = None,
        thumbs: List["types.Thumbnail"] = None
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_ref = file_ref
        self.width = width
        self.height = height
        self.duration = duration
        self.file_name = file_name
        self.mime_type = mime_type
        self.supports_streaming = supports_streaming
        self.file_size = file_size
        self.date = date
        self.ttl_seconds = ttl_seconds
        self.thumbs = thumbs

    @staticmethod
    def _parse(
        client,
        video: "raw.types.Document",
        video_attributes: "raw.types.DocumentAttributeVideo",
        file_name: str,
        ttl_seconds: int = None
    ) -> "Video":
        return Video(
            file_id=encode_file_id(
                pack(
                    "<iiqq",
                    4,
                    video.dc_id,
                    video.id,
                    video.access_hash
                )
            ),
            file_ref=encode_file_ref(video.file_reference),
            width=video_attributes.w,
            height=video_attributes.h,
            duration=video_attributes.duration,
            file_name=file_name,
            mime_type=video.mime_type,
            supports_streaming=video_attributes.supports_streaming,
            file_size=video.size,
            date=video.date,
            ttl_seconds=ttl_seconds,
            thumbs=types.Thumbnail._parse(client, video),
            client=client
        )
