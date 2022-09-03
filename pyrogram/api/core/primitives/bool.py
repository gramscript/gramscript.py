

from io import BytesIO

from ..object import Object


class BoolFalse(Object):
    ID = 0xbc799737
    value = False

    @classmethod
    def read(cls, *args) -> bool:
        return cls.value

    def __new__(cls) -> bytes:
        return int.to_bytes(cls.ID, 4, "little")


class BoolTrue(BoolFalse):
    ID = 0x997275b5
    value = True


class Bool(Object):
    @classmethod
    def read(cls, b: BytesIO) -> bool:
        return int.from_bytes(b.read(4), "little") == BoolTrue.ID

    def __new__(cls, value: bool) -> BoolTrue or BoolFalse:
        return BoolTrue() if value else BoolFalse()
