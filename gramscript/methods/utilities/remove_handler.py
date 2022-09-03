from gramscript.scaffold import Scaffold
from gramscript.handlers.handler import Handler
from gramscript.handlers import DisconnectHandler
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


class RemoveHandler(Scaffold):
    def remove_handler(self, handler: "Handler", group: int = 0):
        """Remove a previously-registered update handler.

        Make sure to provide the right group where the handler was added in. You can use the return value of the
        :meth:`~gramscript.Client.add_handler` method, a tuple of *(handler, group)*, and pass it directly.

        Parameters:
            handler (``Handler``):
                The handler to be removed.

            group (``int``, *optional*):
                The group identifier, defaults to 0.

        Example:
            .. code-block:: python
                :emphasize-lines: 11

                from gramscript import Client, MessageHandler

                def dump(client, message):
                    print(message)

                app = Client("my_account")

                handler = app.add_handler(MessageHandler(dump))

                # Starred expression to unpack (handler, group)
                app.remove_handler(*handler)

                app.run()
        """
        if isinstance(handler, DisconnectHandler):
            self.disconnect_handler = None
        else:
            self.dispatcher.remove_handler(handler, group)
