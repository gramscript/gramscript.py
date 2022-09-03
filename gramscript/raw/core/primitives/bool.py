from ..tl_object import TLObject
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


class BoolFalse(bytes, TLObject):
    ID = 0xBC799737
    value = False

    @classmethod
    def read(cls, *args: Any) -> bool:
        return cls.value

    def __new__(cls) -> bytes:  # type: ignore
        return cls.ID.to_bytes(4, "little")


class BoolTrue(BoolFalse):
    ID = 0x997275B5
    value = True


class Bool(bytes, TLObject):
    @classmethod
    def read(cls, data: BytesIO, *args: Any) -> bool:
        return int.from_bytes(data.read(4), "little") == BoolTrue.ID

    def __new__(cls, value: bool) -> bytes:  # type: ignore
        return BoolTrue() if value else BoolFalse()
