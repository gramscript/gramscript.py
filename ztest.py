
from gramscript import TeleBot
bot = TeleBot("5582426331:AAHEv_idaYL9KWwQTLKXbgy5P23PJnjo7AI")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
