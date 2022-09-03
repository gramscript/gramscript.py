

from io import BytesIO

from ..object import Object


class Int(Object):
    SIZE = 4

    @classmethod
    def read(cls, b: BytesIO, signed: bool = True) -> int:
        return int.from_bytes(b.read(cls.SIZE), "little", signed=signed)

    def __new__(cls, value: int, signed: bool = True) -> bytes:
        return int.to_bytes(value, cls.SIZE, "little", signed=signed)


class Long(Int):
    SIZE = 8

    # TODO: PyCharm can't infer types when overriding parent's __new__ and is showing unnecessary warnings.
    # Add this to shut warnings down
    def __new__(cls, *args):
        return super().__new__(cls, *args)


class Int128(Int):
    SIZE = 16


class Int256(Int):
    SIZE = 32
