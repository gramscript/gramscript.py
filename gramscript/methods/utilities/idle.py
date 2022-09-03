import signal
import logging
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


log = logging.getLogger(__name__)

loop = asyncio.get_event_loop()
event = asyncio.Event()


async def idle():
    """Block the main script execution until a signal is received.

    This function will run indefinitely in order to block the main script execution and prevent it from
    exiting while having client(s) that are still running in the background.

    It is useful for event-driven application only, that are, applications which react upon incoming Telegram
    updates through handlers, rather than executing a set of methods sequentially.

    The way gramscript works, it will keep your handlers in a pool of worker threads, which are executed concurrently
    outside the main thread; calling idle() will ensure the client(s) will be kept alive by not letting the main
    script to end, until you decide to quit.

    Once a signal is received (e.g.: from CTRL+C) the function will terminate and your main script will continue.
    Don't forget to call :meth:`~gramscript.Client.stop` for each running client before the script ends.

    Example:
        .. code-block:: python
            :emphasize-lines: 13

            from gramscript import Client, idle

            app1 = Client("account1")
            app2 = Client("account2")
            app3 = Client("account3")

            ...  # Set handlers up

            app1.start()
            app2.start()
            app3.start()

            idle()

            app1.stop()
            app2.stop()
            app3.stop()
    """

    def handler():
        log.info("Stop signal received")
        event.set()

    asyncio.get_event_loop().add_signal_handler(signal.SIGINT, handler)

    log.info("Idle started")
    await event.wait()

    log.info("Idle stopped")
    event.clear()
