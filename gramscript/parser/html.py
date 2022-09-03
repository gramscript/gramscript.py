from . import utils
from gramscript.errors import PeerIdInvalid
from gramscript import raw
import gramscript
from typing import Union
from html.parser import HTMLParser
import re
import logging
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


log = logging.getLogger(__name__)


class Parser(HTMLParser):
    MENTION_RE = re.compile(r"tg://user\?id=(\d+)")

    def __init__(self, client: "gramscript.Client"):
        super().__init__()

        self.client = client

        self.text = ""
        self.entities = []
        self.tag_entities = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        extra = {}

        if tag in ["b", "strong"]:
            entity = raw.types.MessageEntityBold
        elif tag in ["i", "em"]:
            entity = raw.types.MessageEntityItalic
        elif tag == "u":
            entity = raw.types.MessageEntityUnderline
        elif tag in ["s", "del", "strike"]:
            entity = raw.types.MessageEntityStrike
        elif tag == "blockquote":
            entity = raw.types.MessageEntityBlockquote
        elif tag == "code":
            entity = raw.types.MessageEntityCode
        elif tag == "pre":
            entity = raw.types.MessageEntityPre
            extra["language"] = ""
        elif tag == "a":
            url = attrs.get("href", "")

            mention = Parser.MENTION_RE.match(url)

            if mention:
                entity = raw.types.InputMessageEntityMentionName
                extra["user_id"] = int(mention.group(1))
            else:
                entity = raw.types.MessageEntityTextUrl
                extra["url"] = url
        else:
            return

        if tag not in self.tag_entities:
            self.tag_entities[tag] = []

        self.tag_entities[tag].append(
            entity(offset=len(self.text), length=0, **extra))

    def handle_data(self, data):
        data = html.unescape(data)

        for entities in self.tag_entities.values():
            for entity in entities:
                entity.length += len(data)

        self.text += data

    def handle_endtag(self, tag):
        try:
            self.entities.append(self.tag_entities[tag].pop())
        except (KeyError, IndexError):
            line, offset = self.getpos()
            offset += 1

            log.warning(
                f"Unmatched closing tag </{tag}> at line {line}:{offset}")
        else:
            if not self.tag_entities[tag]:
                self.tag_entities.pop(tag)

    def error(self, message):
        pass


class HTML:
    def __init__(self, client: Union["gramscript.Client", None]):
        self.client = client

    async def parse(self, text: str):
        # Strip whitespace characters from the end of the message, but preserve closing tags
        text = re.sub(r"\s*(</[\w\W]*>)\s*$", r"\1", text)

        parser = Parser(self.client)
        parser.feed(utils.add_surrogates(text))
        parser.close()

        if parser.tag_entities:
            unclosed_tags = []

            for tag, entities in parser.tag_entities.items():
                unclosed_tags.append(f"<{tag}> (x{len(entities)})")

            log.warning(f"Unclosed tags: {', '.join(unclosed_tags)}")

        entities = []

        for entity in parser.entities:
            if isinstance(entity, raw.types.InputMessageEntityMentionName):
                try:
                    if self.client is not None:
                        entity.user_id = await self.client.resolve_peer(entity.user_id)
                except PeerIdInvalid:
                    continue

            entities.append(entity)

        return {
            "message": utils.remove_surrogates(parser.text),
            "entities": sorted(entities, key=lambda e: e.offset)
        }

    @staticmethod
    def unparse(text: str, entities: list):
        text = utils.add_surrogates(text)

        entities_offsets = []

        for entity in entities:
            entity_type = entity.type
            start = entity.offset
            end = start + entity.length

            if entity_type in ("bold", "italic", "underline", "strike"):
                start_tag = f"<{entity_type[0]}>"
                end_tag = "f</{entity_type[0]}>"
            elif entity_type in ("code", "pre", "blockquote"):
                start_tag = f"<{entity_type}>"
                end_tag = f"</{entity_type}>"
            elif entity_type == "text_link":
                url = entity.url
                start_tag = f'<a href="{url}">'
                end_tag = "</a>"
            elif entity_type == "text_mention":
                user = entity.user
                start_tag = f'<a href="tg://user?id={user.id}">'
                end_tag = "</a>"
            else:
                continue

            entities_offsets.append((start_tag, start,))
            entities_offsets.append((end_tag, end,))

        # sorting by offset (desc)
        entities_offsets.sort(key=lambda x: -x[1])

        for entity, offset in entities_offsets:
            text = text[:offset] + entity + text[offset:]

        return utils.remove_surrogates(text)
