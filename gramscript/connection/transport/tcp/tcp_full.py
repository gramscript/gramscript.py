

import logging
from binascii import crc32
from struct import pack, unpack

from .tcp import TCP

log = logging.getLogger(__name__)


class TCPFull(TCP):
    def __init__(self, proxy: type):
        super().__init__(proxy)
        self.seq_no = None

    def connect(self, address: tuple):
        super().connect(address)
        self.seq_no = 0
        log.info("Connected{}!".format(
            " with proxy" if self.proxy_enabled else ""))

    def sendall(self, data: bytes, *args):
        # 12 = packet_length (4), seq_no (4), crc32 (4) (at the end)
        data = pack("<II", len(data) + 12, self.seq_no) + data
        data += pack("<I", crc32(data))
        self.seq_no += 1

        super().sendall(data)

    def recvall(self, length: int = 0) -> bytes or None:
        length = super().recvall(4)

        if length is None:
            return None

        packet = super().recvall(unpack("<I", length)[0] - 4)

        if packet is None:
            return None

        packet = length + packet  # Whole data + checksum
        checksum = packet[-4:]  # Checksum is at the last 4 bytes
        packet = packet[:-4]  # Data without checksum

        if crc32(packet) != unpack("<I", checksum)[0]:
            return None

        return packet[8:]  # Skip packet_length (4) and tcp_seq_no (4)
