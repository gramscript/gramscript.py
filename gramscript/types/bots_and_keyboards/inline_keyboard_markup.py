from ..object import Object
from gramscript import types
from gramscript import raw
from typing import List
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


class InlineKeyboardMarkup(Object):
    """An inline keyboard that appears right next to the message it belongs to.

    Parameters:
        inline_keyboard (List of List of :obj:`~gramscript.types.InlineKeyboardButton`):
            List of button rows, each represented by a List of InlineKeyboardButton objects.
    """

    def __init__(self, inline_keyboard: List[List["types.InlineKeyboardButton"]]):
        super().__init__()

        self.inline_keyboard = inline_keyboard

    @staticmethod
    def read(o):
        inline_keyboard = []

        for i in o.rows:
            row = []

            for j in i.buttons:
                row.append(types.InlineKeyboardButton.read(j))

            inline_keyboard.append(row)

        return InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard
        )

    def write(self):
        return raw.types.ReplyInlineMarkup(
            rows=[raw.types.KeyboardButtonRow(
                buttons=[j.write() for j in i]
            ) for i in self.inline_keyboard]
        )
