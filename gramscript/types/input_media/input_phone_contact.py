from ..object import Object
from gramscript.session.internals import MsgId
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


class InputPhoneContact(Object):
    """A Phone Contact to be added in your Telegram address book.
    It is intended to be used with :meth:`~gramscript.Client.add_contacts()`

    Parameters:
        phone (``str``):
            Contact's phone number

        first_name (``str``):
            Contact's first name

        last_name (``str``, *optional*):
            Contact's last name
    """

    def __init__(self, phone: str, first_name: str, last_name: str = ""):
        super().__init__(None)

    def __new__(cls,
                phone: str,
                first_name: str,
                last_name: str = ""):
        return raw.types.InputPhoneContact(
            client_id=MsgId(),
            phone="+" + phone.strip("+"),
            first_name=first_name,
            last_name=last_name
        )
