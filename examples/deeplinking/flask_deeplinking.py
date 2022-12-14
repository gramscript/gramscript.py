import sys
from flask import Flask, request
import gramscript
from gramscript.loop import OrderedWebhook

"""
$ python2.7 flask_deeplinking.py <bot_username> <token> <listening_port> https://<domain>/webhook

Webhook path is '/webhook'.
Initial webpage is '/link'.

1. Open browser, visit: `https://<domain>/link`
2. Click on the link
3. On Telegram conversation, click on the `START` button
4. Bot should receive a message `/start ghijk`, where `ghijk` is the payload embedded in the link.
   You may use this payload to identify the user, then his Telegram `chat_id`.
"""

key_id_map = {'ghijk': 123}


def handle(msg):
    content_type, chat_type, chat_id = gramscript.glance(msg)
    print('Chat Message:', content_type, chat_type, chat_id)

    if content_type == 'text':
        text = msg['text']
        print('Text:', text)

        if text.startswith('/start'):
            try:
                command, payload = text.split(' ')

                print('Payload:', payload)
                print('User ID:', key_id_map[payload])
                print('chat_id:', chat_id)

            except ValueError:
                print('No payload, or more than one chunk of payload')

            except KeyError:
                print('Invalid key, no corresponding User ID')


BOT_USERNAME = sys.argv[1]
TOKEN = sys.argv[2]
PORT = int(sys.argv[3])
URL = sys.argv[4]

app = Flask(__name__)
bot = gramscript.Bot(TOKEN)
webhook = OrderedWebhook(bot, handle)


@app.route('/link', methods=['GET', 'POST'])
def display_link():
    first_key_in_database = key_id_map.items()[0][0]
    return '<a href="https://telegram.me/%s?start=%s">Open conversation with bot</a>' % (BOT_USERNAME, first_key_in_database)


@app.route('/webhook', methods=['GET', 'POST'])
def pass_update():
    webhook.feed(request.data)
    return 'OK'


if __name__ == '__main__':
    try:
        bot.setWebhook(URL)
    # Sometimes it would raise this error, but webhook still set successfully.
    except gramscript.exception.TooManyRequestsError:
        pass

    webhook.run_as_thread()
    app.run(port=PORT, debug=True)
