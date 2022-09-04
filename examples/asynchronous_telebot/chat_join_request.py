import asyncio
from gramscript.async_telebot import AsyncTeleBot

import gramscript
bot = AsyncTeleBot('TOKEN')


@bot.chat_join_request_handler()
async def make_some(message: gramscript.types.ChatJoinRequest):
    await bot.send_message(message.chat.id, 'I accepted a new user!')
    await bot.approve_chat_join_request(message.chat.id, message.from_user.id)

asyncio.run(bot.polling())
