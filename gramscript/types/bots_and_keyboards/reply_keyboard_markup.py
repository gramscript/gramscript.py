from ..object import Object
from gramscript import types
from gramscript import raw
from typing import List, Union
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


class ReplyKeyboardMarkup(Object):
    """A custom keyboard with reply options.

    Parameters:
        keyboard (List of List of :obj:`~gramscript.types.KeyboardButton`):
            List of button rows, each represented by a List of KeyboardButton objects.

        resize_keyboard (``bool``, *optional*):
            Requests clients to resize the keyboard vertically for optimal fit (e.g., make the keyboard smaller if
            there are just two rows of buttons). Defaults to false, in which case the custom keyboard is always of
            the same height as the app's standard keyboard.

        one_time_keyboard (``bool``, *optional*):
            Requests clients to hide the keyboard as soon as it's been used. The keyboard will still be available,
            but clients will automatically display the usual letter-keyboard in the chat – the user can press a
            special button in the input field to see the custom keyboard again. Defaults to false.

        selective (``bool``, *optional*):
            Use this parameter if you want to show the keyboard to specific users only. Targets:
            1) users that are @mentioned in the text of the Message object;
            2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.
            Example: A user requests to change the bot's language, bot replies to the request with a keyboard to
            select the new language. Other users in the group don't see the keyboard.
    """

    def __init__(
        self,
        keyboard: List[List[Union["types.KeyboardButton", str]]],
        resize_keyboard: bool = None,
        one_time_keyboard: bool = None,
        selective: bool = None
    ):
        super().__init__()

        self.keyboard = keyboard
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.selective = selective

    @staticmethod
    def read(kb):
        keyboard = []

        for i in kb.rows:
            row = []

            for j in i.buttons:
                row.append(types.KeyboardButton.read(j))

            keyboard.append(row)

        return ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=kb.resize,
            one_time_keyboard=kb.single_use,
            selective=kb.selective
        )

    def write(self):
        return raw.types.ReplyKeyboardMarkup(
            rows=[raw.types.KeyboardButtonRow(
                buttons=[
                    types.KeyboardButton(j).write()
                    if isinstance(j, str) else j.write()
                    for j in i
                ]
            ) for i in self.keyboard],
            resize=self.resize_keyboard or None,
            single_use=self.one_time_keyboard or None,
            selective=self.selective or None
        )
