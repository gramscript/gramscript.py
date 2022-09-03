from gramscript.scaffold import Scaffold
from gramscript import utils
from gramscript import types
from gramscript import raw
from typing import List
import logging
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


class GetDialogs(Scaffold):
    async def get_dialogs(
        self,
        offset_date: int = 0,
        limit: int = 100,
        pinned_only: bool = False
    ) -> List["types.Dialog"]:
        """Get a chunk of the user's dialogs.

        You can get up to 100 dialogs at once.
        For a more convenient way of getting a user's dialogs see :meth:`~gramscript.Client.iter_dialogs`.

        Parameters:
            offset_date (``int``):
                The offset date in Unix time taken from the top message of a :obj:`~gramscript.types.Dialog`.
                Defaults to 0. Valid for non-pinned dialogs only.

            limit (``str``, *optional*):
                Limits the number of dialogs to be retrieved.
                Defaults to 100. Valid for non-pinned dialogs only.

            pinned_only (``bool``, *optional*):
                Pass True if you want to get only pinned dialogs.
                Defaults to False.

        Returns:
            List of :obj:`~gramscript.types.Dialog`: On success, a list of dialogs is returned.

        Example:
            .. code-block:: python

                # Get first 100 dialogs
                app.get_dialogs()

                # Get pinned dialogs
                app.get_dialogs(pinned_only=True)
        """

        if pinned_only:
            r = await self.send(raw.functions.messages.GetPinnedDialogs(folder_id=0))
        else:
            r = await self.send(
                raw.functions.messages.GetDialogs(
                    offset_date=offset_date,
                    offset_id=0,
                    offset_peer=raw.types.InputPeerEmpty(),
                    limit=limit,
                    hash=0,
                    exclude_pinned=True
                )
            )

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}

        messages = {}

        for message in r.messages:
            to_id = message.to_id

            if isinstance(to_id, raw.types.PeerUser):
                if message.out:
                    chat_id = to_id.user_id
                else:
                    chat_id = message.from_id
            else:
                chat_id = utils.get_peer_id(to_id)

            messages[chat_id] = await types.Message._parse(self, message, users, chats)

        parsed_dialogs = []

        for dialog in r.dialogs:
            if not isinstance(dialog, raw.types.Dialog):
                continue

            parsed_dialogs.append(types.Dialog._parse(
                self, dialog, messages, users, chats))

        return types.List(parsed_dialogs)
