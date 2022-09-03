

from datetime import datetime
from io import BytesIO

from . import FutureSalt
from .object import Object
from .primitives import Int, Long


class FutureSalts(Object):
    ID = 0xae500895

    def __init__(self, req_msg_id: int, now: int or datetime, salts: list):
        self.req_msg_id = req_msg_id
        self.now = now
        self.salts = salts

    @staticmethod
    def read(b: BytesIO, *args) -> "FutureSalts":
        req_msg_id = Long.read(b)
        now = datetime.fromtimestamp(Int.read(b))

        count = Int.read(b)
        salts = [FutureSalt.read(b) for _ in range(count)]

        return FutureSalts(req_msg_id, now, salts)
