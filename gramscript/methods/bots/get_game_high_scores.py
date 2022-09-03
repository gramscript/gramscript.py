from gramscript.scaffold import Scaffold
from gramscript import types
from gramscript import raw
from typing import Union, List
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


class GetGameHighScores(Scaffold):
    async def get_game_high_scores(
        self,
        user_id: Union[int, str],
        chat_id: Union[int, str],
        message_id: int = None
    ) -> List["types.GameHighScore"]:
        """Get data for high score tables.

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            chat_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                Required if inline_message_id is not specified.

            message_id (``int``, *optional*):
                Identifier of the sent message.
                Required if inline_message_id is not specified.

        Returns:
            List of :obj:`~gramscript.types.GameHighScore`: On success.

        Example:
            .. code-block:: python

                scores = app.get_game_high_scores(user_id, chat_id, message_id)
                print(scores)
        """
        # TODO: inline_message_id

        r = await self.send(
            raw.functions.messages.GetGameHighScores(
                peer=await self.resolve_peer(chat_id),
                id=message_id,
                user_id=await self.resolve_peer(user_id)
            )
        )

        return types.List(types.GameHighScore._parse(self, score, r.users) for score in r.scores)
