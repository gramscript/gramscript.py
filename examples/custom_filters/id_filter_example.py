import gramscript
from gramscript import custom_filters

bot = gramscript.TeleBot('token')


# Chat id can be private or supergroups.
# chat_id checks id corresponds to your list or not.
@bot.message_handler(chat_id=[12345678], commands=['admin'])
def admin_rep(message):
    bot.send_message(message.chat.id, "You are allowed to use this command.")


@bot.message_handler(commands=['admin'])
def not_admin(message):
    bot.send_message(
        message.chat.id, "You are not allowed to use this command")


# Do not forget to register
bot.add_custom_filter(custom_filters.ChatFilter())

bot.infinity_polling()
