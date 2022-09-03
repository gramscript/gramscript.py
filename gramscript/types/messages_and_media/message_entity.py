from ..object import Object
from gramscript import types
from gramscript import raw
import gramscript
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


class MessageEntity(Object):
    """One special entity in a text message.
    For example, hashtags, usernames, URLs, etc.

    Parameters:
        type (``str``):
            Type of the entity.
            Can be "mention" (@username), "hashtag", "cashtag", "bot_command", "url", "email", "phone_number", "bold"
            (bold text), "italic" (italic text), "code" (monowidth string), "pre" (monowidth block), "text_link"
            (for clickable text URLs), "text_mention" (for custom text mentions based on users' identifiers).

        offset (``int``):
            Offset in UTF-16 code units to the start of the entity.

        length (``int``):
            Length of the entity in UTF-16 code units.

        url (``str``, *optional*):
            For "text_link" only, url that will be opened after user taps on the text.

        user (:obj:`~gramscript.types.User`, *optional*):
            For "text_mention" only, the mentioned user.
    """

    ENTITIES = {
        raw.types.MessageEntityMention.ID: "mention",
        raw.types.MessageEntityHashtag.ID: "hashtag",
        raw.types.MessageEntityCashtag.ID: "cashtag",
        raw.types.MessageEntityBotCommand.ID: "bot_command",
        raw.types.MessageEntityUrl.ID: "url",
        raw.types.MessageEntityEmail.ID: "email",
        raw.types.MessageEntityBold.ID: "bold",
        raw.types.MessageEntityItalic.ID: "italic",
        raw.types.MessageEntityCode.ID: "code",
        raw.types.MessageEntityPre.ID: "pre",
        raw.types.MessageEntityUnderline.ID: "underline",
        raw.types.MessageEntityStrike.ID: "strike",
        raw.types.MessageEntityBlockquote.ID: "blockquote",
        raw.types.MessageEntityTextUrl.ID: "text_link",
        raw.types.MessageEntityMentionName.ID: "text_mention",
        raw.types.MessageEntityPhone.ID: "phone_number"
    }

    def __init__(
        self,
        *,
        client: "gramscript.Client" = None,
        type: str,
        offset: int,
        length: int,
        url: str = None,
        user: "types.User" = None
    ):
        super().__init__(client)

        self.type = type
        self.offset = offset
        self.length = length
        self.url = url
        self.user = user

    @staticmethod
    def _parse(client, entity, users: dict) -> "MessageEntity" or None:
        type = MessageEntity.ENTITIES.get(entity.ID, None)

        if type is None:
            return None

        return MessageEntity(
            type=type,
            offset=entity.offset,
            length=entity.length,
            url=getattr(entity, "url", None),
            user=types.User._parse(client, users.get(
                getattr(entity, "user_id", None), None)),
            client=client
        )
