from gramscript.scaffold import Scaffold
from gramscript.errors import PeerIdInvalid
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


class DeleteContacts(Scaffold):
    async def delete_contacts(
        self,
        ids: List[int]
    ):
        """Delete contacts from your Telegram address book.

        Parameters:
            ids (List of ``int``):
                A list of unique identifiers for the target users.
                Can be an ID (int), a username (string) or phone number (string).

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                app.delete_contacts([user_id1, user_id2, user_id3])
        """
        contacts = []

        for i in ids:
            try:
                input_user = await self.resolve_peer(i)
            except PeerIdInvalid:
                continue
            else:
                if isinstance(input_user, raw.types.InputPeerUser):
                    contacts.append(input_user)

        return await self.send(
            raw.functions.contacts.DeleteContacts(
                id=contacts
            )
        )
