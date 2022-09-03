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


class SetGameScore(Scaffold):
    async def set_game_score(
        self,
        user_id: Union[int, str],
        score: int,
        force: bool = None,
        disable_edit_message: bool = None,
        chat_id: Union[int, str] = None,
        message_id: int = None
    ) -> Union["types.Message", bool]:
        # inline_message_id: str = None):  TODO Add inline_message_id
        """Set the score of the specified user in a game.

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            score (``int``):
                New score, must be non-negative.

            force (``bool``, *optional*):
                Pass True, if the high score is allowed to decrease.
                This can be useful when fixing mistakes or banning cheaters.

            disable_edit_message (``bool``, *optional*):
                Pass True, if the game message should not be automatically edited to include the current scoreboard.

            chat_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                Required if inline_message_id is not specified.

            message_id (``int``, *optional*):
                Identifier of the sent message.
                Required if inline_message_id is not specified.

        Returns:
            :obj:`~gramscript.types.Message` | ``bool``: On success, if the message was sent by the bot, the edited
            message is returned, True otherwise.

        Example:
            .. code-block:: python

                # Set new score
                app.set_game_score(user_id, 1000)

                # Force set new score
                app.set_game_score(user_id, 25, force=True)
        """
        r = await self.send(
            raw.functions.messages.SetGameScore(
                peer=await self.resolve_peer(chat_id),
                score=score,
                id=message_id,
                user_id=await self.resolve_peer(user_id),
                force=force or None,
                edit_message=not disable_edit_message or None
            )
        )

        for i in r.updates:
            if isinstance(i, (raw.types.UpdateEditMessage,
                              raw.types.UpdateEditChannelMessage)):
                return await types.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats}
                )

        return True
