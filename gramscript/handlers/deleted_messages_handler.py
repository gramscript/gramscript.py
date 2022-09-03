from .handler import Handler
from gramscript.types import Message
from gramscript.filters import Filter
import gramscript
from typing import List, Callable
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


class DeletedMessagesHandler(Handler):
    """The deleted messages handler class. Used to handle deleted messages coming from any chat
    (private, group, channel). It is intended to be used with :meth:`~gramscript.Client.add_handler`

    For a nicer way to register this handler, have a look at the
    :meth:`~gramscript.Client.on_deleted_messages` decorator.

    Parameters:
        callback (``callable``):
            Pass a function that will be called when one or more messages have been deleted.
            It takes *(client, messages)* as positional arguments (look at the section below for a detailed description).

        filters (:obj:`Filters`):
            Pass one or more filters to allow only a subset of messages to be passed
            in your callback function.

    Other parameters:
        client (:obj:`~gramscript.Client`):
            The Client itself, useful when you want to call other API methods inside the message handler.

        messages (List of :obj:`~gramscript.types.Message`):
            The deleted messages, as list.
    """

    def __init__(self, callback: Callable, filters: Filter = None):
        super().__init__(callback, filters)

    async def check(self, client: "gramscript.Client", messages: List[Message]):
        return await super().check(client, messages[0])
