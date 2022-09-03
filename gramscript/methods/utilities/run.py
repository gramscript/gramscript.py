from gramscript.scaffold import Scaffold
from gramscript.methods.utilities.idle import idle
import inspect
import asyncio
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


class Run(Scaffold):
    def run(self, coroutine=None):
        """Start the client, idle the main script and finally stop the client.

        This is a convenience method that calls :meth:`~gramscript.Client.start`, :meth:`~gramscript.idle` and
        :meth:`~gramscript.Client.stop` in sequence. It makes running a client less verbose, but is not suitable in case
        you want to run more than one client in a single main script, since :meth:`~gramscript.idle` will block after
        starting the own client.

        Raises:
            ConnectionError: In case you try to run an already started client.

        Example:
            .. code-block:: python
                :emphasize-lines: 7

                from gramscript import Client

                app = Client("my_account")

                ...  # Set handlers up

                app.run()
        """
        loop = asyncio.get_event_loop()
        run = loop.run_until_complete

        if coroutine is not None:
            run(coroutine)
        else:
            if inspect.iscoroutinefunction(self.start):
                run(self.start())
                run(idle())
                run(self.stop())
            else:
                self.start()
                run(idle())
                self.stop()
