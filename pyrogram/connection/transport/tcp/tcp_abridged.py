

import logging

from .tcp import TCP

log = logging.getLogger(__name__)


class TCPAbridged(TCP):
    def __init__(self, proxy: type):
        super().__init__(proxy)
        self.is_first_packet = None

    def connect(self, address: tuple):
        super().connect(address)
        self.is_first_packet = True
        log.info("Connected{}!".format(
            " with proxy" if self.proxy_enabled else ""))

    def sendall(self, data: bytes, *args):
        length = len(data) // 4

        data = (
            bytes([length]) + data
            if length <= 126
            else b"\x7f" + int.to_bytes(length, 3, "little") + data
        )

        if self.is_first_packet:
            data = b"\xef" + data
            self.is_first_packet = False

        super().sendall(data)

    def recvall(self, length: int = 0) -> bytes or None:
        length = super().recvall(1)

        if length is None:
            return None

        if length == b"\x7f":
            length = super().recvall(3)

            if length is None:
                return None

        return super().recvall(int.from_bytes(length, "little") * 4)
