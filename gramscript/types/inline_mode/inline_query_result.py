from ..object import Object
from gramscript import types
from uuid import uuid4
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


"""- :obj:`~gramscript.types.InlineQueryResultCachedAudio`
    - :obj:`~gramscript.types.InlineQueryResultCachedDocument`
    - :obj:`~gramscript.types.InlineQueryResultCachedGif`
    - :obj:`~gramscript.types.InlineQueryResultCachedMpeg4Gif`
    - :obj:`~gramscript.types.InlineQueryResultCachedPhoto`
    - :obj:`~gramscript.types.InlineQueryResultCachedSticker`
    - :obj:`~gramscript.types.InlineQueryResultCachedVideo`
    - :obj:`~gramscript.types.InlineQueryResultCachedVoice`
    - :obj:`~gramscript.types.InlineQueryResultAudio`
    - :obj:`~gramscript.types.InlineQueryResultContact`
    - :obj:`~gramscript.types.InlineQueryResultGame`
    - :obj:`~gramscript.types.InlineQueryResultDocument`
    - :obj:`~gramscript.types.InlineQueryResultGif`
    - :obj:`~gramscript.types.InlineQueryResultLocation`
    - :obj:`~gramscript.types.InlineQueryResultMpeg4Gif`
    - :obj:`~gramscript.types.InlineQueryResultPhoto`
    - :obj:`~gramscript.types.InlineQueryResultVenue`
    - :obj:`~gramscript.types.InlineQueryResultVideo`
    - :obj:`~gramscript.types.InlineQueryResultVoice`"""


class InlineQueryResult(Object):
    """One result of an inline query.

    gramscript currently supports results of the following types:

    - :obj:`~gramscript.types.InlineQueryResultArticle`
    - :obj:`~gramscript.types.InlineQueryResultPhoto`
    - :obj:`~gramscript.types.InlineQueryResultAnimation`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: "types.InputMessageContent",
        reply_markup: "types.InlineKeyboardMarkup"
    ):
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self):
        pass
