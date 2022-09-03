from .inline_session import get_session
from gramscript.scaffold import Scaffold
from gramscript import utils
from gramscript import types
from gramscript import raw
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


class EditInlineReplyMarkup(Scaffold):
    async def edit_inline_reply_markup(
        self,
        inline_message_id: str,
        reply_markup: "types.InlineKeyboardMarkup" = None
    ) -> bool:
        """Edit only the reply markup of inline messages sent via the bot (for inline bots).

        Parameters:
            inline_message_id (``str``):
                Identifier of the inline message.

            reply_markup (:obj:`~gramscript.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                from gramscript import InlineKeyboardMarkup, InlineKeyboardButton

                # Bots only
                app.edit_inline_reply_markup(
                    inline_message_id,
                    InlineKeyboardMarkup([[
                        InlineKeyboardButton("New button", callback_data="new_data")]]))
        """

        unpacked = utils.unpack_inline_message_id(inline_message_id)
        dc_id = unpacked.dc_id

        session = get_session(self, dc_id)

        return await session.send(
            raw.functions.messages.EditInlineBotMessage(
                id=unpacked,
                reply_markup=reply_markup.write() if reply_markup else None,
            )
        )
