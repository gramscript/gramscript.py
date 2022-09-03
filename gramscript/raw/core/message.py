from .tl_object import TLObject
from .primitives.int import Int, Long
from typing import Any
from io import BytesIO
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


class Message(TLObject):
    # hex(crc32(b"message msg_id:long seqno:int bytes:int body:Object = Message"))
    ID = 0x5BB8E511

    __slots__ = ["msg_id", "seq_no", "length", "body"]

    QUALNAME = "Message"

    def __init__(self, body: TLObject, msg_id: int, seq_no: int, length: int):
        self.msg_id = msg_id
        self.seq_no = seq_no
        self.length = length
        self.body = body

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "Message":
        msg_id = Long.read(data)
        seq_no = Int.read(data)
        length = Int.read(data)
        body = data.read(length)

        return Message(TLObject.read(BytesIO(body)), msg_id, seq_no, length)

    def write(self, *args: Any) -> bytes:
        b = BytesIO()

        b.write(Long(self.msg_id))
        b.write(Int(self.seq_no))
        b.write(Int(self.length))
        b.write(self.body.write())

        return b.getvalue()
