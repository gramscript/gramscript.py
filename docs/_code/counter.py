import sys
import time
import gramscript
from gramscript.loop import MessageLoop
from gramscript.delegate import pave_event_space, per_chat_id, create_open


class MessageCounter(gramscript.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._count = 0

    def on_chat_message(self, msg):
        self._count += 1
        self.sender.sendMessage(self._count)


TOKEN = sys.argv[1]  # get token from command-line

bot = gramscript.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=10),
])
MessageLoop(bot).run_as_thread()

while 1:
    time.sleep(10)
