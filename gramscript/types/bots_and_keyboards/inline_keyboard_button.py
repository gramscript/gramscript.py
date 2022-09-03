from ..object import Object
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


class InlineKeyboardButton(Object):
    """One button of an inline keyboard.

    You must use exactly one of the optional fields.

    Parameters:
        text (``str``):
            Label text on the button.

        callback_data (``str`` | ``bytes``, *optional*):
            Data to be sent in a callback query to the bot when button is pressed, 1-64 bytes.

        url (``str``, *optional*):
            HTTP url to be opened when button is pressed.

        switch_inline_query (``str``, *optional*):
            If set, pressing the button will prompt the user to select one of their chats, open that chat and insert
            the bot's username and the specified inline query in the input field. Can be empty, in which case just
            the bot's username will be inserted.Note: This offers an easy way for users to start using your bot in
            inline mode when they are currently in a private chat with it. Especially useful when combined with
            switch_pm… actions – in this case the user will be automatically returned to the chat they switched from,
            skipping the chat selection screen.

        switch_inline_query_current_chat (``str``, *optional*):
            If set, pressing the button will insert the bot's username and the specified inline query in the current
            chat's input field. Can be empty, in which case only the bot's username will be inserted.This offers a
            quick way for the user to open your bot in inline mode in the same chat – good for selecting something
            from multiple options.
    """

    # TODO: Add callback_game and pay fields

    def __init__(
        self,
        text: str,
        callback_data: Union[str, bytes] = None,
        url: str = None,
        switch_inline_query: str = None,
        switch_inline_query_current_chat: str = None,
        callback_game: "types.CallbackGame" = None
    ):
        super().__init__()

        self.text = str(text)
        self.url = url
        self.callback_data = callback_data
        self.switch_inline_query = switch_inline_query
        self.switch_inline_query_current_chat = switch_inline_query_current_chat
        self.callback_game = callback_game
        # self.pay = pay

    @staticmethod
    def read(o):
        if isinstance(o, raw.types.KeyboardButtonUrl):
            return InlineKeyboardButton(
                text=o.text,
                url=o.url
            )

        if isinstance(o, raw.types.KeyboardButtonCallback):
            # Try decode data to keep it as string, but if fails, fallback to bytes so we don't lose any information,
            # instead of decoding by ignoring/replacing errors.
            try:
                data = o.data.decode()
            except UnicodeDecodeError:
                data = o.data

            return InlineKeyboardButton(
                text=o.text,
                callback_data=data
            )

        if isinstance(o, raw.types.KeyboardButtonSwitchInline):
            if o.same_peer:
                return InlineKeyboardButton(
                    text=o.text,
                    switch_inline_query_current_chat=o.query
                )
            else:
                return InlineKeyboardButton(
                    text=o.text,
                    switch_inline_query=o.query
                )

        if isinstance(o, raw.types.KeyboardButtonGame):
            return InlineKeyboardButton(
                text=o.text,
                callback_game=types.CallbackGame()
            )

    def write(self):
        if self.callback_data is not None:
            # Telegram only wants bytes, but we are allowed to pass strings too, for convenience.
            data = bytes(self.callback_data, "utf-8") if isinstance(
                self.callback_data, str) else self.callback_data
            return raw.types.KeyboardButtonCallback(text=self.text, data=data)

        if self.url is not None:
            return raw.types.KeyboardButtonUrl(text=self.text, url=self.url)

        if self.switch_inline_query is not None:
            return raw.types.KeyboardButtonSwitchInline(text=self.text, query=self.switch_inline_query)

        if self.switch_inline_query_current_chat is not None:
            return raw.types.KeyboardButtonSwitchInline(
                text=self.text,
                query=self.switch_inline_query_current_chat,
                same_peer=True
            )

        if self.callback_game is not None:
            return raw.types.KeyboardButtonGame(text=self.text)
