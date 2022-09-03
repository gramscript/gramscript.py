from .handler import Handler
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


class RawUpdateHandler(Handler):
    """The Raw Update handler class. Used to handle raw updates. It is intended to be used with
    :meth:`~gramscript.Client.add_handler`

    For a nicer way to register this handler, have a look at the
    :meth:`~gramscript.Client.on_raw_update` decorator.

    Parameters:
        callback (``callable``):
            A function that will be called when a new update is received from the server. It takes
            *(client, update, users, chats)* as positional arguments (look at the section below for
            a detailed description).

    Other Parameters:
        client (:obj:`~gramscript.Client`):
            The Client itself, useful when you want to call other API methods inside the update handler.

        update (``Update``):
            The received update, which can be one of the many single Updates listed in the *updates*
            field you see in the :obj:`~gramscript.types.Update` type.

        users (``dict``):
            Dictionary of all :obj:`~gramscript.types.User` mentioned in the update.
            You can access extra info about the user (such as *first_name*, *last_name*, etc...) by using
            the IDs you find in the *update* argument (e.g.: *users[1768841572]*).

        chats (``dict``):
            Dictionary of all :obj:`~gramscript.types.Chat` and
            :obj:`Channel <gramscript.api.types.Channel>` mentioned in the update.
            You can access extra info about the chat (such as *title*, *participants_count*, etc...)
            by using the IDs you find in the *update* argument (e.g.: *chats[1701277281]*).

    Note:
        The following Empty or Forbidden types may exist inside the *users* and *chats* dictionaries.
        They mean you have been blocked by the user or banned from the group/channel.

        - :obj:`UserEmpty <gramscript.api.types.UserEmpty>`
        - :obj:`ChatEmpty <gramscript.api.types.ChatEmpty>`
        - :obj:`ChatForbidden <gramscript.api.types.ChatForbidden>`
        - :obj:`ChannelForbidden <gramscript.api.types.ChannelForbidden>`
    """

    def __init__(self, callback: callable):
        super().__init__(callback)
