from .tcp import TCP
from struct import pack, unpack
from binascii import crc32
import logging
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


class TCPFull(TCP):
    def __init__(self, ipv6: bool, proxy: dict):
        super().__init__(ipv6, proxy)

        self.seq_no = None

    async def connect(self, address: tuple):
        await super().connect(address)
        self.seq_no = 0

    async def send(self, data: bytes, *args):
        data = pack("<II", len(data) + 12, self.seq_no) + data
        data += pack("<I", crc32(data))
        self.seq_no += 1

        await super().send(data)

    async def recv(self, length: int = 0) -> bytes or None:
        length = await super().recv(4)

        if length is None:
            return None

        packet = await super().recv(unpack("<I", length)[0] - 4)

        if packet is None:
            return None

        packet = length + packet
        checksum = packet[-4:]
        packet = packet[:-4]

        if crc32(packet) != unpack("<I", checksum)[0]:
            return None

        return packet[8:]
