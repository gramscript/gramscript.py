

from datetime import datetime
from io import BytesIO

from .object import Object
from .primitives import Int, Long


class FutureSalt(Object):
    ID = 0x0949d9dc

    def __init__(self, valid_since: int or datetime, valid_until: int or datetime, salt: int):
        self.valid_since = valid_since
        self.valid_until = valid_until
        self.salt = salt

    @staticmethod
    def read(b: BytesIO, *args) -> "FutureSalt":
        valid_since = datetime.fromtimestamp(Int.read(b))
        valid_until = datetime.fromtimestamp(Int.read(b))
        salt = Long.read(b)

        return FutureSalt(valid_since, valid_until, salt)
