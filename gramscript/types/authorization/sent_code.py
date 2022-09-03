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


class SentCode(Object):
    """Contains info on a sent confirmation code.

    Parameters:
        type (``str``):
            Type of the current sent code.
            Can be *"app"* (code sent via Telegram), *"sms"* (code sent via SMS), *"call"* (code sent via voice call) or
            *"flash_call"* (code is in the last 5 digits of the caller's phone number).

        phone_code_hash (``str``):
            Confirmation code identifier useful for the next authorization steps (either
            :meth:`~gramscript.Client.sign_in` or :meth:`~gramscript.Client.sign_up`).

        next_type (``str``):
            Type of the next code to be sent with :meth:`~gramscript.Client.resend_code`.
            Can be *"sms"* (code will be sent via SMS), *"call"* (code will be sent via voice call) or *"flash_call"*
            (code will be in the last 5 digits of caller's phone number).

        timeout (``int``):
            Delay in seconds before calling :meth:`~gramscript.Client.resend_code`.
    """

    def __init__(
        self, *,
        type: str,
        phone_code_hash: str,
        next_type: str = None,
        timeout: int = None
    ):
        super().__init__()

        self.type = type
        self.phone_code_hash = phone_code_hash
        self.next_type = next_type
        self.timeout = timeout

    @staticmethod
    def _parse(sent_code: raw.types.auth.SentCode) -> "SentCode":
        type = sent_code.type

        if isinstance(type, raw.types.auth.SentCodeTypeApp):
            type = "app"
        elif isinstance(type, raw.types.auth.SentCodeTypeSms):
            type = "sms"
        elif isinstance(type, raw.types.auth.SentCodeTypeCall):
            type = "call"
        elif isinstance(type, raw.types.auth.SentCodeTypeFlashCall):
            type = "flash_call"

        next_type = sent_code.next_type

        if isinstance(next_type, raw.types.auth.CodeTypeSms):
            next_type = "sms"
        elif isinstance(next_type, raw.types.auth.CodeTypeCall):
            next_type = "call"
        elif isinstance(next_type, raw.types.auth.CodeTypeFlashCall):
            next_type = "flash_call"

        return SentCode(
            type=type,
            phone_code_hash=sent_code.phone_code_hash,
            next_type=next_type,
            timeout=sent_code.timeout
        )
