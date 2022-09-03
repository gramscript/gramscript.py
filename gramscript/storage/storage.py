from typing import List, Tuple
import struct
import base64
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


class Storage:
    SESSION_STRING_FORMAT = ">B?256sI?"
    SESSION_STRING_SIZE = 351

    def __init__(self, name: str):
        self.name = name

    async def open(self):
        raise NotImplementedError

    async def save(self):
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError

    async def delete(self):
        raise NotImplementedError

    async def update_peers(self, peers: List[Tuple[int, int, str, str, str]]):
        raise NotImplementedError

    async def get_peer_by_id(self, peer_id: int):
        raise NotImplementedError

    async def get_peer_by_username(self, username: str):
        raise NotImplementedError

    async def get_peer_by_phone_number(self, phone_number: str):
        raise NotImplementedError

    async def dc_id(self, value: int = object):
        raise NotImplementedError

    async def test_mode(self, value: bool = object):
        raise NotImplementedError

    async def auth_key(self, value: bytes = object):
        raise NotImplementedError

    async def date(self, value: int = object):
        raise NotImplementedError

    async def user_id(self, value: int = object):
        raise NotImplementedError

    async def is_bot(self, value: bool = object):
        raise NotImplementedError

    async def export_session_string(self):
        return base64.urlsafe_b64encode(
            struct.pack(
                self.SESSION_STRING_FORMAT,
                await self.dc_id(),
                await self.test_mode(),
                await self.auth_key(),
                await self.user_id(),
                await self.is_bot()
            )
        ).decode().rstrip("=")
