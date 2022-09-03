from gramscript.scaffold import Scaffold
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


class Restart(Scaffold):
    async def restart(self, block: bool = True):
        """Restart the Client.

        This method will first call :meth:`~gramscript.Client.stop` and then :meth:`~gramscript.Client.start` in a row in
        order to restart a client using a single method.

        Parameters:
            block (``bool``, *optional*):
                Blocks the code execution until the client has been restarted. It is useful with ``block=False`` in case
                you want to restart the own client *within* an handler in order not to cause a deadlock.
                Defaults to True.

        Returns:
            :obj:`~gramscript.Client`: The restarted client itself.

        Raises:
            ConnectionError: In case you try to restart a stopped Client.

        Example:
            .. code-block:: python
                :emphasize-lines: 8

                from gramscript import Client

                app = Client("my_account")
                app.start()

                ...  # Call API methods

                app.restart()

                ...  # Call other API methods

                app.stop()
        """

        async def do_it():
            await self.stop()
            await self.start()

        if block:
            await do_it()
        else:
            self.loop.create_task(do_it())

        return self
