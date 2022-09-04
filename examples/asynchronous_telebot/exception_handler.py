
import asyncio
import gramscript
from gramscript.async_telebot import AsyncTeleBot


import logging

logger = gramscript.logger
gramscript.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.


class ExceptionHandler(gramscript.ExceptionHandler):
    def handle(self, exception):
        logger.error(exception)


bot = AsyncTeleBot('TOKEN', exception_handler=ExceptionHandler())


@bot.message_handler(commands=['photo'])
async def photo_send(message: gramscript.types.Message):
    await bot.send_message(message.chat.id, 'Hi, this is an example of exception handlers.')
    raise Exception('test')  # Exception goes to ExceptionHandler if it is set


asyncio.run(bot.polling())
