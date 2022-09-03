

from io import BytesIO

from .object import Object
from .primitives import Int, Long


class Message(Object):
    # hex(crc32(b"message msg_id:long seqno:int bytes:int body:Object = Message"))
    ID = 0x5bb8e511

    def __init__(self, body: Object, msg_id: int, seq_no: int, length: int):
        self.msg_id = msg_id
        self.seq_no = seq_no
        self.length = length
        self.body = body

    @staticmethod
    def read(b: BytesIO, *args) -> "Message":
        msg_id = Long.read(b)
        seq_no = Int.read(b)
        length = Int.read(b)
        body = b.read(length)

        return Message(Object.read(BytesIO(body)), msg_id, seq_no, length)

    def write(self) -> bytes:
        b = BytesIO()

        b.write(Long(self.msg_id))
        b.write(Int(self.seq_no))
        b.write(Int(self.length))
        b.write(self.body.write())

        return b.getvalue()
