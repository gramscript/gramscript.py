from gramscript.scaffold import Scaffold
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


class AddContacts(Scaffold):
    async def add_contacts(
        self,
        contacts: List["types.InputPhoneContact"]
    ):
        """Add contacts to your Telegram address book.

        Parameters:
            contacts (List of :obj:`~gramscript.types.InputPhoneContact`):
                The contact list to be added

        Returns:
            :obj:`types.contacts.ImportedContacts`

        Example:
            .. code-block:: python

                from gramscript import InputPhoneContact

                app.add_contacts([
                    InputPhoneContact("39123456789", "Foo"),
                    InputPhoneContact("38987654321", "Bar"),
                    InputPhoneContact("01234567891", "Baz")])
        """
        imported_contacts = await self.send(
            raw.functions.contacts.ImportContacts(
                contacts=contacts
            )
        )

        return imported_contacts
