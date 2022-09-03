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


class Audio(Object):
    """An audio file to be treated as music by the Telegram clients.

    Parameters:
        file_id (``str``):
            Unique identifier for this file.

        file_ref (``str``):
            Up to date file reference.

        duration (``int``):
            Duration of the audio in seconds as defined by sender.

        file_name (``str``, *optional*):
            Audio file name.

        mime_type (``str``, *optional*):
            MIME type of the file as defined by sender.

        file_size (``int``, *optional*):
            File size.

        date (``int``, *optional*):
            Date the audio was sent in Unix time.

        performer (``str``, *optional*):
            Performer of the audio as defined by sender or by audio tags.

        title (``str``, *optional*):
            Title of the audio as defined by sender or by audio tags.

        thumbs (List of :obj:`~gramscript.types.Thumbnail`, *optional*):
            Thumbnails of the music file album cover.
    """

    def __init__(
        self,
        *,
        client: "gramscript.Client" = None,
        file_id: str,
        file_ref: str,
        duration: int,
        file_name: str = None,
        mime_type: str = None,
        file_size: int = None,
        date: int = None,
        performer: str = None,
        title: str = None,
        thumbs: List["types.Thumbnail"] = None
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_ref = file_ref
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date
        self.duration = duration
        self.performer = performer
        self.title = title
        self.thumbs = thumbs

    @staticmethod
    def _parse(
        client,
        audio: "raw.types.Document",
        audio_attributes: "raw.types.DocumentAttributeAudio",
        file_name: str
    ) -> "Audio":
        return Audio(
            file_id=encode_file_id(
                pack(
                    "<iiqq",
                    9,
                    audio.dc_id,
                    audio.id,
                    audio.access_hash
                )
            ),
            file_ref=encode_file_ref(audio.file_reference),
            duration=audio_attributes.duration,
            performer=audio_attributes.performer,
            title=audio_attributes.title,
            mime_type=audio.mime_type,
            file_size=audio.size,
            file_name=file_name,
            date=audio.date,
            thumbs=types.Thumbnail._parse(client, audio),
            client=client
        )
