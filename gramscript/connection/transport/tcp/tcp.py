import time
import socket
import logging
import ipaddress
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


try:
    import socks
except ImportError as e:
    e.msg = (
        "PySocks is missing and gramscript can't run without. "
        "Please install it using \"pip3 install pysocks\"."
    )

    raise e

log = logging.getLogger(__name__)


class TCP:
    TIMEOUT = 10

    def __init__(self, ipv6: bool, proxy: dict):
        self.socket = None

        self.reader = None  # type: asyncio.StreamReader
        self.writer = None  # type: asyncio.StreamWriter

        self.lock = asyncio.Lock()

        if proxy.get("enabled", False):
            hostname = proxy.get("hostname", None)
            port = proxy.get("port", None)

            try:
                ip_address = ipaddress.ip_address(hostname)
            except ValueError:
                self.socket = socks.socksocket(socket.AF_INET)
            else:
                if isinstance(ip_address, ipaddress.IPv6Address):
                    self.socket = socks.socksocket(socket.AF_INET6)
                else:
                    self.socket = socks.socksocket(socket.AF_INET)

            self.socket.set_proxy(
                proxy_type=socks.SOCKS5,
                addr=hostname,
                port=port,
                username=proxy.get("username", None),
                password=proxy.get("password", None)
            )

            log.info(f"Using proxy {hostname}:{port}")
        else:
            self.socket = socks.socksocket(
                socket.AF_INET6 if ipv6
                else socket.AF_INET
            )

        self.socket.settimeout(TCP.TIMEOUT)

    async def connect(self, address: tuple):
        self.socket.connect(address)
        self.reader, self.writer = await asyncio.open_connection(sock=self.socket)

    def close(self):
        try:
            self.writer.close()
        except AttributeError:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            finally:
                # A tiny sleep placed here helps avoiding .recv(n) hanging until the timeout.
                # This is a workaround that seems to fix the occasional delayed stop of a client.
                time.sleep(0.001)
                self.socket.close()

    async def send(self, data: bytes):
        async with self.lock:
            self.writer.write(data)
            await self.writer.drain()

    async def recv(self, length: int = 0):
        data = b""

        while len(data) < length:
            try:
                chunk = await asyncio.wait_for(
                    self.reader.read(length - len(data)),
                    TCP.TIMEOUT
                )
            except (OSError, asyncio.TimeoutError):
                return None
            else:
                if chunk:
                    data += chunk
                else:
                    return None

        return data
