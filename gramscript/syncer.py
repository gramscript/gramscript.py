import time
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


class Syncer:
    INTERVAL = 20

    clients = {}
    event = None
    lock = None

    @classmethod
    async def add(cls, client):
        if cls.event is None:
            cls.event = asyncio.Event()

        if cls.lock is None:
            cls.lock = asyncio.Lock()

        async with cls.lock:
            await cls.sync(client)

            cls.clients[id(client)] = client

            if len(cls.clients) == 1:
                cls.start()

    @classmethod
    async def remove(cls, client):
        async with cls.lock:
            await cls.sync(client)

            del cls.clients[id(client)]

            if len(cls.clients) == 0:
                cls.stop()

    @classmethod
    def start(cls):
        cls.event.clear()
        asyncio.get_event_loop().create_task(cls.worker())

    @classmethod
    def stop(cls):
        cls.event.set()

    @classmethod
    async def worker(cls):
        while True:
            try:
                await asyncio.wait_for(cls.event.wait(), cls.INTERVAL)
            except asyncio.TimeoutError:
                async with cls.lock:
                    for client in cls.clients.values():
                        await cls.sync(client)
            else:
                break

    @classmethod
    async def sync(cls, client):
        try:
            start = time.time()
            await client.storage.save()
        except Exception as e:
            log.critical(e, exc_info=True)
        else:
            log.info(
                f'Synced "{client.storage.name}" in {(time.time() - start) * 1000:.6} ms')
