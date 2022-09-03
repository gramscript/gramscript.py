from gramscript.scaffold import Scaffold
from gramscript import types
from gramscript import raw
from typing import Union, Iterable, List
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


class ForwardMessages(Scaffold):
    async def forward_messages(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_ids: Union[int, Iterable[int]],
        disable_notification: bool = None,
        as_copy: bool = False,
        remove_caption: bool = False,
        schedule_date: int = None
    ) -> List["types.Message"]:
        """Forward messages of any kind.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            from_chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the source chat where the original message was sent.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_ids (``iterable``):
                A list of Message identifiers in the chat specified in *from_chat_id* or a single message id.
                Iterators and Generators are also accepted.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            as_copy (``bool``, *optional*):
                Pass True to forward messages without the forward header (i.e.: send a copy of the message content so
                that it appears as originally sent by you).
                Defaults to False.

            remove_caption (``bool``, *optional*):
                If set to True and *as_copy* is enabled as well, media captions are not preserved when copying the
                message. Has no effect if *as_copy* is not enabled.
                Defaults to False.

            schedule_date (``int``, *optional*):
                Date when the message will be automatically sent. Unix time.

        Returns:
            :obj:`~gramscript.types.Message` | List of :obj:`~gramscript.types.Message`: In case *message_ids* was an
            integer, the single forwarded message is returned, otherwise, in case *message_ids* was an iterable,
            the returned value will be a list of messages, even if such iterable contained just a single element.

        Example:
            .. code-block:: python
                :emphasize-lines: 2,5,8

                # Forward a single message
                app.forward_messages("me", "gramscript", 20)

                # Forward multiple messages at once
                app.forward_messages("me", "gramscript", [3, 20, 27])

                # Forward messages as copy
                app.forward_messages("me", "gramscript", 20, as_copy=True)
        """

        is_iterable = not isinstance(message_ids, int)
        message_ids = list(message_ids) if is_iterable else [message_ids]

        if as_copy:
            forwarded_messages = []

            for chunk in [message_ids[i:i + 200] for i in range(0, len(message_ids), 200)]:
                messages = await self.get_messages(chat_id=from_chat_id, message_ids=chunk)

                for message in messages:
                    forwarded_messages.append(
                        await message.forward(
                            chat_id,
                            disable_notification=disable_notification,
                            as_copy=True,
                            remove_caption=remove_caption,
                            schedule_date=schedule_date
                        )
                    )

            return types.List(forwarded_messages) if is_iterable else forwarded_messages[0]
        else:
            r = await self.send(
                raw.functions.messages.ForwardMessages(
                    to_peer=await self.resolve_peer(chat_id),
                    from_peer=await self.resolve_peer(from_chat_id),
                    id=message_ids,
                    silent=disable_notification or None,
                    random_id=[self.rnd_id() for _ in message_ids],
                    schedule_date=schedule_date
                )
            )

            forwarded_messages = []

            users = {i.id: i for i in r.users}
            chats = {i.id: i for i in r.chats}

            for i in r.updates:
                if isinstance(i, (raw.types.UpdateNewMessage,
                                  raw.types.UpdateNewChannelMessage,
                                  raw.types.UpdateNewScheduledMessage)):
                    forwarded_messages.append(
                        await types.Message._parse(
                            self, i.message,
                            users, chats
                        )
                    )

            return types.List(forwarded_messages) if is_iterable else forwarded_messages[0]
