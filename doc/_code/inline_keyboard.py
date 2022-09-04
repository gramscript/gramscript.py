import sys
import time
import gramscript
from gramscript.loop import MessageLoop
from gramscript.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


def on_chat_message(msg):
    content_type, chat_type, chat_id = gramscript.glance(msg)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Press me', callback_data='press')],
    ])

    bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)


def on_callback_query(msg):
    query_id, from_id, query_data = gramscript.glance(
        msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text='Got it')


TOKEN = sys.argv[1]  # get token from command-line

bot = gramscript.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)
