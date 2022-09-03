from gramscript.scaffold import Scaffold
from gramscript import utils
from gramscript import types
from gramscript import raw
from typing import Union, Iterable, List
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


# TODO: Rewrite using a flag for replied messages and have message_ids non-optional


class GetMessages(Scaffold):
    async def get_messages(
        self,
        chat_id: Union[int, str],
        message_ids: Union[int, Iterable[int]] = None,
        reply_to_message_ids: Union[int, Iterable[int]] = None,
        replies: int = 1
    ) -> Union["types.Message", List["types.Message"]]:
        """Get one or more messages from a chat by using message identifiers.

        You can retrieve up to 200 messages at once.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_ids (``iterable``, *optional*):
                Pass a single message identifier or a list of message ids (as integers) to get the content of the
                message themselves. Iterators and Generators are also accepted.

            reply_to_message_ids (``iterable``, *optional*):
                Pass a single message identifier or a list of message ids (as integers) to get the content of
                the previous message you replied to using this message. Iterators and Generators are also accepted.
                If *message_ids* is set, this argument will be ignored.

            replies (``int``, *optional*):
                The number of subsequent replies to get for each message.
                Pass 0 for no reply at all or -1 for unlimited replies.
                Defaults to 1.

        Returns:
            :obj:`~gramscript.types.Message` | List of :obj:`~gramscript.types.Message`: In case *message_ids* was an
            integer, the single requested message is returned, otherwise, in case *message_ids* was an iterable, the
            returned value will be a list of messages, even if such iterable contained just a single element.

        Example:
            .. code-block:: python

                # Get one message
                app.get_messages("gramscriptchat", 51110)

                # Get more than one message (list of messages)
                app.get_messages("gramscriptchat", [44625, 51110])

                # Get message by ignoring any replied-to message
                app.get_messages(chat_id, message_id, replies=0)

                # Get message with all chained replied-to messages
                app.get_messages(chat_id, message_id, replies=-1)

                # Get the replied-to message of a message
                app.get_messages(chat_id, reply_to_message_ids=message_id)

        Raises:
            ValueError: In case of invalid arguments.
        """
        ids, ids_type = (
            (message_ids, raw.types.InputMessageID) if message_ids
            else (reply_to_message_ids, raw.types.InputMessageReplyTo) if reply_to_message_ids
            else (None, None)
        )

        if ids is None:
            raise ValueError(
                "No argument supplied. Either pass message_ids or reply_to_message_ids")

        peer = await self.resolve_peer(chat_id)

        is_iterable = not isinstance(ids, int)
        ids = list(ids) if is_iterable else [ids]
        ids = [ids_type(id=i) for i in ids]

        if replies < 0:
            replies = (1 << 31) - 1

        if isinstance(peer, raw.types.InputPeerChannel):
            rpc = raw.functions.channels.GetMessages(channel=peer, id=ids)
        else:
            rpc = raw.functions.messages.GetMessages(id=ids)

        r = await self.send(rpc)

        messages = await utils.parse_messages(self, r, replies=replies)

        return messages if is_iterable else messages[0]
