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


class ChosenInlineResultHandler(Handler):
    """The ChosenInlineResultHandler handler class. Used to handle chosen inline results coming from inline queries.
    It is intended to be used with :meth:`~gramscript.Client.add_handler`

    For a nicer way to register this handler, have a look at the
    :meth:`~gramscript.Client.on_chosen_inline_query` decorator.

    Parameters:
        callback (``callable``):
            Pass a function that will be called when a new chosen inline result arrives.
            It takes *(client, chosen_inline_result)* as positional arguments (look at the section below for a
            detailed description).

        filters (:obj:`Filters`):
            Pass one or more filters to allow only a subset of chosen inline results to be passed
            in your callback function.

    Other parameters:
        client (:obj:`~gramscript.Client`):
            The Client itself, useful when you want to call other API methods inside the message handler.

        chosen_inline_result (:obj:`~gramscript.types.ChosenInlineResult`):
            The received chosen inline result.
    """

    def __init__(self, callback: callable, filters=None):
        super().__init__(callback, filters)
