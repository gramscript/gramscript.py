from time import monotonic
from datetime import datetime
import logging
# MIT License

# Copyright (c) 2022 Gramscript Telegram API

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


log = logging.getLogger(__name__)


class MsgId:
    reference_clock = monotonic()
    last_time = 0
    msg_id_offset = 0
    server_time = 0

    def __new__(cls) -> int:
        now = monotonic() - cls.reference_clock + cls.server_time
        cls.msg_id_offset = cls.msg_id_offset + 4 if now == cls.last_time else 0
        msg_id = int(now * 2 ** 32) + cls.msg_id_offset
        cls.last_time = now

        return msg_id

    @classmethod
    def set_server_time(cls, server_time: int):
        if not cls.server_time:
            cls.server_time = server_time
            log.info(
                f"Time synced: {datetime.utcfromtimestamp(server_time)} UTC")
