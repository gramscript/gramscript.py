from ..object import Object
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


class Restriction(Object):
    """A restriction applied to bots or chats.

    Parameters:
        platform (``str``):
            The platform the restriction is applied to, e.g. "ios", "android"

        reason (``str``):
            The restriction reason, e.g. "porn", "copyright".

        text (``str``):
            The restriction text.
    """

    def __init__(self, *, platform: str, reason: str, text: str):
        super().__init__(None)

        self.platform = platform
        self.reason = reason
        self.text = text

    @staticmethod
    def _parse(restriction: "raw.types.RestrictionReason") -> "Restriction":
        return Restriction(
            platform=restriction.platform,
            reason=restriction.reason,
            text=restriction.text
        )
