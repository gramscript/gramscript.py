from .input_message_content import InputMessageContent
from gramscript.parser import Parser
from gramscript import raw
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


class InputTextMessageContent(InputMessageContent):
    """Content of a text message to be sent as the result of an inline query.

    Parameters:
        message_text (``str``):
            Text of the message to be sent, 1-4096 characters.

        parse_mode (``str``, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.
            Pass "markdown" or "md" to enable Markdown-style parsing only.
            Pass "html" to enable HTML-style parsing only.
            Pass None to completely disable style parsing.

        disable_web_page_preview (``bool``, *optional*):
            Disables link previews for links in this message.
    """

    def __init__(self, message_text: str, parse_mode: Union[str, None] = object, disable_web_page_preview: bool = None):
        super().__init__()

        self.message_text = message_text
        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview

    async def write(self, reply_markup):
        return raw.types.InputBotInlineMessageText(
            no_webpage=self.disable_web_page_preview or None,
            reply_markup=reply_markup.write() if reply_markup else None,
            **await(Parser(None)).parse(self.message_text, self.parse_mode)
        )
