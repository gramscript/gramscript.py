from gramscript.scaffold import Scaffold
from gramscript import raw
from typing import Union, Iterable
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


class DeleteMessages(Scaffold):
    async def delete_messages(
        self,
        chat_id: Union[int, str],
        message_ids: Union[int, Iterable[int]],
        revoke: bool = True
    ) -> bool:
        """Delete messages, including service messages.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_ids (``int`` | ``Iterable[int]``):
                A list of Message identifiers to delete (integers) or a single message id.
                Iterators and Generators are also accepted.

            revoke (``bool``, *optional*):
                Deletes messages on both parts.
                This is only for private cloud chats and normal groups, messages on
                channels and supergroups are always revoked (i.e.: deleted for everyone).
                Defaults to True.

        Returns:
            ``bool``: True on success, False otherwise.

        Example:
            .. code-block:: python

                # Delete one message
                app.delete_messages(chat_id, message_id)

                # Delete multiple messages at once
                app.delete_messages(chat_id, list_of_message_ids)

                # Delete messages only on your side (without revoking)
                app.delete_messages(chat_id, message_id, revoke=False)
        """
        peer = await self.resolve_peer(chat_id)
        message_ids = list(message_ids) if not isinstance(
            message_ids, int) else [message_ids]

        if isinstance(peer, raw.types.InputPeerChannel):
            r = await self.send(
                raw.functions.channels.DeleteMessages(
                    channel=peer,
                    id=message_ids
                )
            )
        else:
            r = await self.send(
                raw.functions.messages.DeleteMessages(
                    id=message_ids,
                    revoke=revoke or None
                )
            )

        # Deleting messages you don't have right onto, won't raise any error.
        # Check for pts_count, which is 0 in case deletes fail.
        return bool(r.pts_count)
