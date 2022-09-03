

import logging
from struct import pack, unpack

from .tcp_abridged import TCP

log = logging.getLogger(__name__)


class TCPIntermediate(TCP):
    def __init__(self, proxy: type):
        super().__init__(proxy)
        self.is_first_packet = None

    def connect(self, address: tuple):
        super().connect(address)
        self.is_first_packet = True
        log.info("Connected{}!".format(
            " with proxy" if self.proxy_enabled else ""))

    def sendall(self, data: bytes, *args):
        length = len(data)
        data = pack("<i", length) + data

        if self.is_first_packet:
            data = b"\xee" * 4 + data
            self.is_first_packet = False

        super().sendall(data)

    def recvall(self, length: int = 0) -> bytes or None:
        length = super().recvall(4)

        if length is None:
            return None

        return super().recvall(unpack("<I", length)[0])
