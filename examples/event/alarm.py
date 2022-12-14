import sys
import time
import gramscript
from gramscript.loop import MessageLoop
from gramscript.delegate import per_chat_id, create_open, pave_event_space

"""
$ python3.6 alarm.py <token>

Send a number which indicates the delay in seconds. The bot will send you an
alarm message after such a delay. It illustrates how to use the built-in
scheduler to schedule custom events for later.

To design a custom event, you first have to invent a *flavor*. To prevent flavors
from colliding with those of Telegram messages, events are given flavors prefixed
with `_` by convention. Then, follow these steps, which are further detailed by
comments in the code:

1. Customize routing table so the correct function gets called on seeing the event
2. Define event-handling function
3. Provide the event spec when scheduling events
"""


class AlarmSetter(gramscript.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(AlarmSetter, self).__init__(*args, **kwargs)

        # 1. Customize the routing table:
        #      On seeing an event of flavor `_alarm`, call `self.on__alarm`.
        # To prevent flavors from colliding with those of Telegram messages,
        # events are given flavors prefixed with `_` by convention. Also by
        # convention is that the event-handling function is named `on_`
        # followed by flavor, leading to the double underscore.
        self.router.routing_table['_alarm'] = self.on__alarm

    # 2. Define event-handling function
    def on__alarm(self, event):
        print(event)  # see what the event object actually looks like
        self.sender.sendMessage('Beep beep, time to wake up!')

    def on_chat_message(self, msg):
        try:
            delay = float(msg['text'])

            # 3. Schedule event
            #      The second argument is the event spec: a 2-tuple of (flavor, dict).
            # Put any custom data in the dict. Retrieve them in the event-handling function.
            self.scheduler.event_later(delay, ('_alarm', {'payload': delay}))
            self.sender.sendMessage(
                'Got it. Alarm is set at %.1f seconds from now.' % delay)
        except ValueError:
            self.sender.sendMessage('Not a number. No alarm set.')


TOKEN = sys.argv[1]

bot = gramscript.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, AlarmSetter, timeout=10),
])
MessageLoop(bot).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)
