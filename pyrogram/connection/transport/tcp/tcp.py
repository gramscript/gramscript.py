

import logging
import socket
from collections import namedtuple

import socks

log = logging.getLogger(__name__)

Proxy = namedtuple("Proxy", ["enabled", "hostname",
                   "port", "username", "password"])


class TCP(socks.socksocket):
    def __init__(self, proxy: Proxy):
        super().__init__()
        self.proxy_enabled = False

        if proxy and proxy.enabled:
            self.proxy_enabled = True

            self.set_proxy(
                proxy_type=socks.SOCKS5,
                addr=proxy.hostname,
                port=proxy.port,
                username=proxy.username,
                password=proxy.password
            )

    def close(self):
        try:
            self.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        finally:
            super().close()

    def recvall(self, length: int) -> bytes or None:
        data = b""

        while len(data) < length:
            try:
                packet = super().recv(length - len(data))
            except OSError:
                return None
            else:
                if packet:
                    data += packet
                else:
                    return None

        return data
