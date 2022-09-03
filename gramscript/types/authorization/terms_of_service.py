from ..object import Object
from gramscript import types
from gramscript import raw
from typing import List
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


class TermsOfService(Object):
    """Telegram's Terms of Service returned by :meth:`~gramscript.Client.sign_in`.

    Parameters:
        id (``str``):
            Terms of Service identifier.

        text (``str``):
            Terms of Service text.

        entities (List of :obj:`~gramscript.types.MessageEntity`):
            Special entities like URLs that appear in the text.
    """

    def __init__(self, *, id: str, text: str, entities: List["types.MessageEntity"]):
        super().__init__()

        self.id = id
        self.text = text
        self.entities = entities

    @staticmethod
    def _parse(terms_of_service: "raw.types.help.TermsOfService") -> "TermsOfService":
        return TermsOfService(
            id=terms_of_service.id.data,
            text=terms_of_service.text,
            entities=[
                types.MessageEntity._parse(None, entity, {})
                for entity in terms_of_service.entities
            ]
        )
