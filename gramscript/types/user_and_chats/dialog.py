from ... import utils
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


class Dialog(Object):
    """A user's dialog.

    Parameters:
        chat (:obj:`~gramscript.types.Chat`):
            Conversation the dialog belongs to.

        top_message (:obj:`~gramscript.types.Message`):
            The last message sent in the dialog at this time.

        unread_messages_count (``int``):
            Amount of unread messages in this dialog.

        unread_mentions_count (``int``):
            Amount of unread messages containing a mention in this dialog.

        unread_mark (``bool``):
            True, if the dialog has the unread mark set.

        is_pinned (``bool``):
            True, if the dialog is pinned.
    """

    def __init__(
        self,
        *,
        client: "gramscript.Client" = None,
        chat: "types.Chat",
        top_message: "types.Message",
        unread_messages_count: int,
        unread_mentions_count: int,
        unread_mark: bool,
        is_pinned: bool
    ):
        super().__init__(client)

        self.chat = chat
        self.top_message = top_message
        self.unread_messages_count = unread_messages_count
        self.unread_mentions_count = unread_mentions_count
        self.unread_mark = unread_mark
        self.is_pinned = is_pinned

    @staticmethod
    def _parse(client, dialog: "raw.types.Dialog", messages, users, chats) -> "Dialog":
        return Dialog(
            chat=types.Chat._parse_dialog(client, dialog.peer, users, chats),
            top_message=messages.get(utils.get_peer_id(dialog.peer)),
            unread_messages_count=dialog.unread_count,
            unread_mentions_count=dialog.unread_mentions_count,
            unread_mark=dialog.unread_mark,
            is_pinned=dialog.pinned,
            client=client
        )
