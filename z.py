import time
import telepot
from telepot.loop import MessageLoop


def handle(msg):
    flavor = telepot.flavor(msg)

    summary = telepot.glance(msg, flavor=flavor)
    print (flavor, summary)


TOKEN = "5582426331:AAHEv_idaYL9KWwQTLKXbgy5P23PJnjo7AI" #sys.argv[1]  # get token from command-line

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)