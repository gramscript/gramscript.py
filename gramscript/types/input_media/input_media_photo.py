from .input_media import InputMedia
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


class InputMediaPhoto(InputMedia):
    """A photo to be sent inside an album.
    It is intended to be used with :obj:`~gramscript.Client.send_media_group`.

    Parameters:
        media (``str``):
            Photo to send.
            Pass a file_id as string to send a photo that exists on the Telegram servers or
            pass a file path as string to upload a new photo that exists on your local machine.
            Sending photo by a URL is currently unsupported.

        file_ref (``str``, *optional*):
            A valid file reference obtained by a recently fetched media message.
            To be used in combination with a file id in case a file reference is needed.

        caption (``str``, *optional*):
            Caption of the photo to be sent, 0-1024 characters

        parse_mode (``str``, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.
            Pass "markdown" or "md" to enable Markdown-style parsing only.
            Pass "html" to enable HTML-style parsing only.
            Pass None to completely disable style parsing.
    """

    def __init__(
        self,
        media: str,
        file_ref: str = None,
        caption: str = "",
        parse_mode: Union[str, None] = object
    ):
        super().__init__(media, file_ref, caption, parse_mode)
