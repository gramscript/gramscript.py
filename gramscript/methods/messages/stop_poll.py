from gramscript.scaffold import Scaffold
from gramscript import types
from gramscript import raw
from typing import Union
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


class StopPoll(Scaffold):
    async def stop_poll(
        self,
        chat_id: Union[int, str],
        message_id: int,
        reply_markup: "types.InlineKeyboardMarkup" = None
    ) -> "types.Poll":
        """Stop a poll which was sent by you.

        Stopped polls can't be reopened and nobody will be able to vote in it anymore.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Identifier of the original message with the poll.

            reply_markup (:obj:`~gramscript.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            :obj:`~gramscript.types.Poll`: On success, the stopped poll with the final results is returned.

        Example:
            .. code-block:: python

                app.stop_poll(chat_id, message_id)
        """
        poll = (await self.get_messages(chat_id, message_id)).poll

        r = await self.send(
            raw.functions.messages.EditMessage(
                peer=await self.resolve_peer(chat_id),
                id=message_id,
                media=raw.types.InputMediaPoll(
                    poll=raw.types.Poll(
                        id=int(poll.id),
                        closed=True,
                        question="",
                        answers=[]
                    )
                ),
                reply_markup=reply_markup.write() if reply_markup else None
            )
        )

        return types.Poll._parse(self, r.updates[0])
