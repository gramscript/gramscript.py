import sys
import time
import gramscript
import gramscript.namedtuple
from gramscript.loop import MessageLoop

"""
$ python2.7 emodi.py <token>

Emodi: An Emoji Unicode Decoder - You send it some emoji, it tells you the unicodes.

Caution: Python's treatment of unicode characters longer than 2 bytes (which
most emojis are) varies across versions and platforms. I have tested this program
on Python2.7.9/Raspbian. If you try it on other versions/platforms, the length-
checking and substring-extraction below may not work as expected.
"""


def handle(msg):
    content_type, chat_type, chat_id = gramscript.glance(msg)
    m = gramscript.namedtuple.Message(**msg)

    if chat_id < 0:
        # group message
        print(f'Received a {content_type} from {m.chat}, by {m.from_}')
    else:
        # private message
        print(f'Received a {content_type} from {m.chat}')

    if content_type == 'text':
        reply = u'First 10 characters:\n' if len(msg['text']) > 10 else ''
        # Length-checking and substring-extraction may work differently
        # depending on Python versions and platforms. See above.

        reply += msg['text'][:10].encode('unicode-escape').decode('ascii')
        bot.sendMessage(chat_id, reply)


TOKEN = sys.argv[1]  # get token from command-line

bot = gramscript.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
