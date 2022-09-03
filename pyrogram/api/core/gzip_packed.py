

from gzip import compress, decompress
from io import BytesIO

from .object import Object
from .primitives import Int, Bytes


class GzipPacked(Object):
    ID = 0x3072cfa1

    def __init__(self, packed_data: Object):
        self.packed_data = packed_data

    @staticmethod
    def read(b: BytesIO, *args) -> "GzipPacked":
        # Return the Object itself instead of a GzipPacked wrapping it
        return Object.read(
            BytesIO(
                decompress(
                    Bytes.read(b)
                )
            )
        )

    def write(self) -> bytes:
        b = BytesIO()

        b.write(Int(self.ID, False))

        b.write(
            Bytes(
                compress(
                    self.packed_data.write()
                )
            )
        )

        return b.getvalue()
