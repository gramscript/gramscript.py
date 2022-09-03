from .inline_query_result import InlineQueryResult
from gramscript import types
from gramscript import raw
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


class InlineQueryResultArticle(InlineQueryResult):
    """Link to an article or web page.

    Parameters:
        title (``str``):
            Title for the result.

        input_message_content (:obj:`~gramscript.types.InputMessageContent`):
            Content of the message to be sent.

        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.

        url (``str``, *optional*):
            URL of the result.

        description (``str``, *optional*):
            Short description of the result.

        thumb_url (``str``, *optional*):
            URL of the thumbnail for the result.

        reply_markup (:obj:`~gramscript.types.InlineKeyboardMarkup`, *optional*):
            Inline keyboard attached to the message.
    """

    def __init__(
        self,
        title: str,
        input_message_content: "types.InputMessageContent",
        id: str = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        url: str = None,
        description: str = None,
        thumb_url: str = None
    ):
        super().__init__("article", id, input_message_content, reply_markup)

        self.title = title
        self.url = url
        self.description = description
        self.thumb_url = thumb_url

    async def write(self):
        return raw.types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            send_message=await self.input_message_content.write(self.reply_markup),
            title=self.title,
            description=self.description,
            url=self.url,
            thumb=raw.types.InputWebDocument(
                url=self.thumb_url,
                size=0,
                mime_type="image/jpeg",
                attributes=[]
            ) if self.thumb_url else None
        )
