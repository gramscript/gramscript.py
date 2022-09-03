from .html import HTML
from . import utils
import gramscript
from typing import Union
import re
import html
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


BOLD_DELIM = "**"
ITALIC_DELIM = "__"
UNDERLINE_DELIM = "--"
STRIKE_DELIM = "~~"
CODE_DELIM = "`"
PRE_DELIM = "```"

MARKDOWN_RE = re.compile(r"({d})|\[(.+?)\]\((.+?)\)".format(
    d="|".join(
        ["".join(i) for i in [
            [rf"\{j}" for j in i]
            for i in [
                PRE_DELIM,
                CODE_DELIM,
                STRIKE_DELIM,
                UNDERLINE_DELIM,
                ITALIC_DELIM,
                BOLD_DELIM
            ]
        ]]
    )))

OPENING_TAG = "<{}>"
CLOSING_TAG = "</{}>"
URL_MARKUP = '<a href="{}">{}</a>'
FIXED_WIDTH_DELIMS = [CODE_DELIM, PRE_DELIM]


class Markdown:
    def __init__(self, client: Union["gramscript.Client", None]):
        self.html = HTML(client)

    async def parse(self, text: str, strict: bool = False):
        if strict:
            text = html.escape(text)

        delims = set()
        is_fixed_width = False

        for i, match in enumerate(re.finditer(MARKDOWN_RE, text)):
            start, _ = match.span()
            delim, text_url, url = match.groups()
            full = match.group(0)

            if delim in FIXED_WIDTH_DELIMS:
                is_fixed_width = not is_fixed_width

            if is_fixed_width and delim not in FIXED_WIDTH_DELIMS:
                continue

            if text_url:
                text = utils.replace_once(
                    text, full, URL_MARKUP.format(url, text_url), start)
                continue

            if delim == BOLD_DELIM:
                tag = "b"
            elif delim == ITALIC_DELIM:
                tag = "i"
            elif delim == UNDERLINE_DELIM:
                tag = "u"
            elif delim == STRIKE_DELIM:
                tag = "s"
            elif delim == CODE_DELIM:
                tag = "code"
            elif delim == PRE_DELIM:
                tag = "pre"
            else:
                continue

            if delim not in delims:
                delims.add(delim)
                tag = OPENING_TAG.format(tag)
            else:
                delims.remove(delim)
                tag = CLOSING_TAG.format(tag)

            text = utils.replace_once(text, delim, tag, start)

        return await self.html.parse(text)

    @staticmethod
    def unparse(text: str, entities: list):
        text = utils.add_surrogates(text)

        entities_offsets = []

        for entity in entities:
            entity_type = entity.type
            start = entity.offset
            end = start + entity.length

            if entity_type == "bold":
                start_tag = end_tag = BOLD_DELIM
            elif entity_type == "italic":
                start_tag = end_tag = ITALIC_DELIM
            elif entity_type == "underline":
                start_tag = end_tag = UNDERLINE_DELIM
            elif entity_type == "strike":
                start_tag = end_tag = STRIKE_DELIM
            elif entity_type == "code":
                start_tag = end_tag = CODE_DELIM
            elif entity_type in ("pre", "blockquote"):
                start_tag = end_tag = PRE_DELIM
            elif entity_type == "text_link":
                url = entity.url
                start_tag = "["
                end_tag = f"]({url})"
            elif entity_type == "text_mention":
                user = entity.user
                start_tag = "["
                end_tag = f"](tg://user?id={user.id})"
            else:
                continue

            entities_offsets.append((start_tag, start,))
            entities_offsets.append((end_tag, end,))

        # sorting by offset (desc)
        entities_offsets.sort(key=lambda x: -x[1])

        for entity, offset in entities_offsets:
            text = text[:offset] + entity + text[offset:]

        return utils.remove_surrogates(text)
