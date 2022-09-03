

from io import BytesIO

from ..object import Object


class Bytes(Object):
    @staticmethod
    def read(b: BytesIO, *args) -> bytes:
        length = int.from_bytes(b.read(1), "little")

        if length <= 253:
            x = b.read(length)
            b.read(-(length + 1) % 4)
        else:
            length = int.from_bytes(b.read(3), "little")
            x = b.read(length)
            b.read(-length % 4)

        return x

    def __new__(cls, value: bytes) -> bytes:
        length = len(value)

        if length <= 253:
            return (
                bytes([length])
                + value
                + bytes(-(length + 1) % 4)
            )
        else:
            return (
                bytes([254])
                + int.to_bytes(length, 3, "little")
                + value
                + bytes(-length % 4)
            )
