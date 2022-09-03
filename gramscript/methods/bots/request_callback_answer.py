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


class RequestCallbackAnswer(Scaffold):
    async def request_callback_answer(
        self,
        chat_id: Union[int, str],
        message_id: int,
        callback_data: Union[str, bytes],
        timeout: int = 10
    ):
        """Request a callback answer from bots.
        This is the equivalent of clicking an inline button containing callback data.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                The message id the inline keyboard is attached on.

            callback_data (``str`` | ``bytes``):
                Callback data associated with the inline button you want to get the answer from.

            timeout (``int``, *optional*):
                Timeout in seconds.

        Returns:
            The answer containing info useful for clients to display a notification at the top of the chat screen
            or as an alert.

        Raises:
            TimeoutError: In case the bot fails to answer within 10 seconds.

        Example:
            .. code-block:: python

                app.request_callback_answer(chat_id, message_id, "callback_data")
        """

        # Telegram only wants bytes, but we are allowed to pass strings too.
        data = bytes(
            callback_data, "utf-8") if isinstance(callback_data, str) else callback_data

        return await self.send(
            raw.functions.messages.GetBotCallbackAnswer(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
                data=data
            ),
            retries=0,
            timeout=timeout
        )
