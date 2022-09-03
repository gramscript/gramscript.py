from ..session.internals import DataCenter
from .transport import *
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


class Connection:
    MAX_RETRIES = 3

    MODES = {
        0: TCPFull,
        1: TCPAbridged,
        2: TCPIntermediate,
        3: TCPAbridgedO,
        4: TCPIntermediateO
    }

    def __init__(self, dc_id: int, test_mode: bool, ipv6: bool, proxy: dict, mode: int = 3):
        self.dc_id = dc_id
        self.test_mode = test_mode
        self.ipv6 = ipv6
        self.proxy = proxy
        self.address = DataCenter(dc_id, test_mode, ipv6)
        self.mode = self.MODES.get(mode, TCPAbridged)

        self.protocol = None  # type: TCP

    async def connect(self):
        for i in range(Connection.MAX_RETRIES):
            self.protocol = self.mode(self.ipv6, self.proxy)

            try:
                log.info("Connecting...")
                await self.protocol.connect(self.address)
            except OSError as e:
                log.warning(e)  # TODO: Remove
                self.protocol.close()
                await asyncio.sleep(1)
            else:
                log.info("Connected! {} DC{} - IPv{} - {}".format(
                    "Test" if self.test_mode else "Production",
                    self.dc_id,
                    "6" if self.ipv6 else "4",
                    self.mode.__name__
                ))
                break
        else:
            log.warning("Connection failed! Trying again...")
            raise TimeoutError

    def close(self):
        self.protocol.close()
        log.info("Disconnected")

    async def send(self, data: bytes):
        try:
            await self.protocol.send(data)
        except Exception:
            raise OSError

    async def recv(self) -> bytes or None:
        return await self.protocol.recv()
