

from io import BytesIO

from ..object import Object


class Null(Object):
    ID = 0x56730bcc

    @staticmethod
    def read(b: BytesIO, *args) -> None:
        return None

    def __new__(cls) -> bytes:
        return int.to_bytes(cls.ID, 4, "little")
