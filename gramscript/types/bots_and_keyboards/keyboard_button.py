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


class KeyboardButton(Object):
    """One button of the reply keyboard.
    For simple text buttons String can be used instead of this object to specify text of the button.
    Optional fields are mutually exclusive.

    Parameters:
        text (``str``):
            Text of the button. If none of the optional fields are used, it will be sent as a message when
            the button is pressed.

        request_contact (``bool``, *optional*):
            If True, the user's phone number will be sent as a contact when the button is pressed.
            Available in private chats only.

        request_location (``bool``, *optional*):
            If True, the user's current location will be sent when the button is pressed.
            Available in private chats only.
    """

    def __init__(
        self,
        text: str,
        request_contact: bool = None,
        request_location: bool = None
    ):
        super().__init__()

        self.text = str(text)
        self.request_contact = request_contact
        self.request_location = request_location

    @staticmethod
    def read(o):
        if isinstance(o, raw.types.KeyboardButton):
            return o.text

        if isinstance(o, raw.types.KeyboardButtonRequestPhone):
            return KeyboardButton(
                text=o.text,
                request_contact=True
            )

        if isinstance(o, raw.types.KeyboardButtonRequestGeoLocation):
            return KeyboardButton(
                text=o.text,
                request_location=True
            )

    def write(self):
        # TODO: Enforce optional args mutual exclusiveness

        if self.request_contact:
            return raw.types.KeyboardButtonRequestPhone(text=self.text)
        elif self.request_location:
            return raw.types.KeyboardButtonRequestGeoLocation(text=self.text)
        else:
            return raw.types.KeyboardButton(text=self.text)
