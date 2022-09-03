from ..object import Object
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


class ReplyKeyboardRemove(Object):
    """Object used to tell clients to remove a bot keyboard.

    Upon receiving a message with this object, Telegram clients will remove the current custom keyboard and display
    the default letter-keyboard. By default, custom keyboards are displayed until a new keyboard is sent by a bot.
    An exception is made for one-time keyboards that are hidden immediately after the user presses a button
    (see ReplyKeyboardMarkup).

    Parameters:
        selective (``bool``, *optional*):
            Use this parameter if you want to remove the keyboard for specific users only. Targets:
            1) users that are @mentioned in the text of the Message object;
            2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.
            Example: A user votes in a poll, bot returns confirmation message in reply to the vote and removes the
            keyboard for that user, while still showing the keyboard with poll options to users who haven't voted yet.
    """

    def __init__(
        self,
        selective: bool = None
    ):
        super().__init__()

        self.selective = selective

    @staticmethod
    def read(o):
        return ReplyKeyboardRemove(
            selective=o.selective
        )

    def write(self):
        return raw.types.ReplyKeyboardHide(
            selective=self.selective or None
        )
