

import logging
import threading
import time

from .transport import *

log = logging.getLogger(__name__)


class Connection:
    MODES = {
        0: TCPFull,
        1: TCPAbridged,
        2: TCPIntermediate
    }

    def __init__(self, ipv4: str, proxy: type, mode: int = 1):
        self.address = (ipv4, 80)
        self.proxy = proxy
        self.mode = self.MODES.get(mode, TCPAbridged)
        self.lock = threading.Lock()
        self.connection = None

    def connect(self):
        while True:
            self.connection = self.mode(self.proxy)

            try:
                log.info("Connecting...")
                self.connection.connect(self.address)
            except OSError:
                self.connection.close()
                time.sleep(1)
            else:
                break

    def close(self):
        self.connection.close()

    def send(self, data: bytes):
        with self.lock:
            self.connection.sendall(data)

    def recv(self) -> bytes or None:
        return self.connection.recvall()
