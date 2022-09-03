

from time import time


class MsgId:
    def __init__(self, delta_time: float = 0.0):
        self.delta_time = delta_time
        self.last_time = 0
        self.offset = 0

    def __call__(self) -> int:
        now = time()
        self.offset = self.offset + 4 if now == self.last_time else 0
        msg_id = int((now + self.delta_time) * 2 ** 32) + self.offset
        self.last_time = now

        return msg_id
