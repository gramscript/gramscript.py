from gramscript.scaffold import Scaffold
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


class SendInlineBotResult(Scaffold):
    async def send_inline_bot_result(
        self,
        chat_id: Union[int, str],
        query_id: int,
        result_id: str,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        hide_via: bool = None
    ):
        """Send an inline bot result.
        Bot results can be retrieved using :meth:`~gramscript.Client.get_inline_bot_results`

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            query_id (``int``):
                Unique identifier for the answered query.

            result_id (``str``):
                Unique identifier for the result that was chosen.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``bool``, *optional*):
                If the message is a reply, ID of the original message.

            hide_via (``bool``):
                Sends the message with *via @bot* hidden.

        Returns:
            :obj:`~gramscript.types.Message`: On success, the sent inline result message is returned.

        Example:
            .. code-block:: python

                app.send_inline_bot_result(chat_id, query_id, result_id)
        """
        return await self.send(
            raw.functions.messages.SendInlineBotResult(
                peer=await self.resolve_peer(chat_id),
                query_id=query_id,
                id=result_id,
                random_id=self.rnd_id(),
                silent=disable_notification or None,
                reply_to_msg_id=reply_to_message_id,
                hide_via=hide_via or None
            )
        )
