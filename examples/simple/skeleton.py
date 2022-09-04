import sys
import time
import gramscript
from gramscript.loop import MessageLoop

"""
$ python2.7 skeleton.py <token>

A skeleton for your gramscript programs.
"""


def handle(msg):
    flavor = gramscript.flavor(msg)

    summary = gramscript.glance(msg, flavor=flavor)
    print(flavor, summary)


TOKEN = sys.argv[1]  # get token from command-line

bot = gramscript.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
