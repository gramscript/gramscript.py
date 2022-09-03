from ..object import Object
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


class InputMedia(Object):
    """Content of a media message to be sent.

    It should be one of:

    - :obj:`~gramscript.types.InputMediaAnimation`
    - :obj:`~gramscript.types.InputMediaDocument`
    - :obj:`~gramscript.types.InputMediaAudio`
    - :obj:`~gramscript.types.InputMediaPhoto`
    - :obj:`~gramscript.types.InputMediaVideo`
    """

    def __init__(self, media: str, file_ref: str, caption: str, parse_mode: str):
        super().__init__()

        self.media = media
        self.file_ref = file_ref
        self.caption = caption
        self.parse_mode = parse_mode
