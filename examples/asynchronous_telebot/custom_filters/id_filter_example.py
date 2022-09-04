import asyncio
from gramscript.async_telebot import AsyncTeleBot
import gramscript
bot = AsyncTeleBot('TOKEN')


# Chat id can be private or supergroups.
# chat_id checks id corresponds to your list or not.
@bot.message_handler(chat_id=[12345678], commands=['admin'])
async def admin_rep(message):
    await bot.send_message(message.chat.id, "You are allowed to use this command.")


@bot.message_handler(commands=['admin'])
async def not_admin(message):
    await bot.send_message(message.chat.id, "You are not allowed to use this command")

# Do not forget to register
bot.add_custom_filter(gramscript.asyncio_filters.ChatFilter())
asyncio.run(bot.polling())
