

from gramscript.api.core import Message, MsgContainer, Object
from gramscript.api.functions import Ping, HttpWait
from gramscript.api.types import MsgsAck
from .msg_id import MsgId
from .seq_no import SeqNo

not_content_related = [Ping, HttpWait, MsgsAck, MsgContainer]


class MsgFactory:
    def __init__(self, msg_id: MsgId):
        self.msg_id = msg_id
        self.seq_no = SeqNo()

    def __call__(self, body: Object) -> Message:
        return Message(
            body,
            self.msg_id(),
            self.seq_no(type(body) not in not_content_related),
            len(body)
        )
