from .markdown import Markdown
from .html import HTML
import gramscript
from typing import Union
from collections import OrderedDict
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


class Parser:
    def __init__(self, client: Union["gramscript.Client", None]):
        self.client = client
        self.html = HTML(client)
        self.markdown = Markdown(client)

    async def parse(self, text: str, mode: Union[str, None] = object):
        text = str(text).strip()

        if mode == object:
            if self.client:
                mode = self.client.parse_mode
            else:
                mode = "combined"

        if mode is None:
            return OrderedDict([
                ("message", text),
                ("entities", [])
            ])

        mode = mode.lower()

        if mode == "combined":
            return await self.markdown.parse(text)

        if mode in ["markdown", "md"]:
            return await self.markdown.parse(text, True)

        if mode == "html":
            return await self.html.parse(text)

        raise ValueError('parse_mode must be one of {} or None. Not "{}"'.format(
            ", ".join(f'"{m}"' for m in gramscript.Client.PARSE_MODES[:-1]),
            mode
        ))

    @staticmethod
    def unparse(text: str, entities: list, is_html: bool):
        if is_html:
            return HTML.unparse(text, entities)
        else:
            return Markdown.unparse(text, entities)
