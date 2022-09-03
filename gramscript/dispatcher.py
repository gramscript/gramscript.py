from gramscript.raw.types import (
    UpdateNewMessage, UpdateNewChannelMessage, UpdateNewScheduledMessage,
    UpdateEditMessage, UpdateEditChannelMessage,
    UpdateDeleteMessages, UpdateDeleteChannelMessages,
    UpdateBotCallbackQuery, UpdateInlineBotCallbackQuery,
    UpdateUserStatus, UpdateBotInlineQuery, UpdateMessagePoll,
    UpdateBotInlineSend
)
from gramscript.handlers import (
    CallbackQueryHandler, MessageHandler, DeletedMessagesHandler,
    UserStatusHandler, RawUpdateHandler, InlineQueryHandler, PollHandler,
    ChosenInlineResultHandler
)
from gramscript import utils
import gramscript
from collections import OrderedDict
import logging
import inspect
import asyncio

# MIT License

# Copyright (c) 2022 Gramscript Telegram API

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


log = logging.getLogger(__name__)


class Dispatcher:
    NEW_MESSAGE_UPDATES = (
        UpdateNewMessage,
        UpdateNewChannelMessage,
        UpdateNewScheduledMessage
    )

    EDIT_MESSAGE_UPDATES = (
        UpdateEditMessage,
        UpdateEditChannelMessage,
    )

    DELETE_MESSAGES_UPDATES = (
        UpdateDeleteMessages,
        UpdateDeleteChannelMessages
    )

    CALLBACK_QUERY_UPDATES = (
        UpdateBotCallbackQuery,
        UpdateInlineBotCallbackQuery
    )

    MESSAGE_UPDATES = NEW_MESSAGE_UPDATES + EDIT_MESSAGE_UPDATES

    def __init__(self, client: "gramscript.Client"):
        self.client = client
        self.loop = asyncio.get_event_loop()

        self.handler_worker_tasks = []
        self.locks_list = []

        self.updates_queue = asyncio.Queue()
        self.groups = OrderedDict()

        async def message_parser(update, users, chats):
            return await gramscript.types.Message._parse(
                self.client, update.message, users, chats,
                isinstance(update, UpdateNewScheduledMessage)
            ), MessageHandler

        async def deleted_messages_parser(update, users, chats):
            return utils.parse_deleted_messages(self.client, update), DeletedMessagesHandler

        async def callback_query_parser(update, users, chats):
            return await gramscript.types.CallbackQuery._parse(self.client, update, users), CallbackQueryHandler

        async def user_status_parser(update, users, chats):
            return gramscript.types.User._parse_user_status(self.client, update), UserStatusHandler

        async def inline_query_parser(update, users, chats):
            return gramscript.types.InlineQuery._parse(self.client, update, users), InlineQueryHandler

        async def poll_parser(update, users, chats):
            return gramscript.types.Poll._parse_update(self.client, update), PollHandler

        async def chosen_inline_result_parser(update, users, chats):
            return gramscript.types.ChosenInlineResult._parse(self.client, update, users), ChosenInlineResultHandler

        self.update_parsers = {
            Dispatcher.MESSAGE_UPDATES: message_parser,
            Dispatcher.DELETE_MESSAGES_UPDATES: deleted_messages_parser,
            Dispatcher.CALLBACK_QUERY_UPDATES: callback_query_parser,
            (UpdateUserStatus,): user_status_parser,
            (UpdateBotInlineQuery,): inline_query_parser,
            (UpdateMessagePoll,): poll_parser,
            (UpdateBotInlineSend,): chosen_inline_result_parser
        }

        self.update_parsers = {key: value for key_tuple,
                               value in self.update_parsers.items() for key in key_tuple}

    async def start(self):
        if not self.client.no_updates:
            for i in range(self.client.workers):
                self.locks_list.append(asyncio.Lock())

                self.handler_worker_tasks.append(
                    self.loop.create_task(
                        self.handler_worker(self.locks_list[-1]))
                )

            logging.info(f"Started {self.client.workers} HandlerTasks")

    async def stop(self):
        if not self.client.no_updates:
            for i in range(self.client.workers):
                self.updates_queue.put_nowait(None)

            for i in self.handler_worker_tasks:
                await i

            self.handler_worker_tasks.clear()
            self.groups.clear()

            logging.info(f"Stopped {self.client.workers} HandlerTasks")

    def add_handler(self, handler, group: int):
        async def fn():
            for lock in self.locks_list:
                await lock.acquire()

            try:
                if group not in self.groups:
                    self.groups[group] = []
                    self.groups = OrderedDict(sorted(self.groups.items()))

                self.groups[group].append(handler)
            finally:
                for lock in self.locks_list:
                    lock.release()

        self.loop.create_task(fn())

    def remove_handler(self, handler, group: int):
        async def fn():
            for lock in self.locks_list:
                await lock.acquire()

            try:
                if group not in self.groups:
                    raise ValueError(
                        f"Group {group} does not exist. Handler was not removed.")

                self.groups[group].remove(handler)
            finally:
                for lock in self.locks_list:
                    lock.release()

        self.loop.create_task(fn())

    async def handler_worker(self, lock):
        while True:
            packet = await self.updates_queue.get()

            if packet is None:
                break

            try:
                update, users, chats = packet
                parser = self.update_parsers.get(type(update), None)

                parsed_update, handler_type = (
                    await parser(update, users, chats)
                    if parser is not None
                    else (None, type(None))
                )

                async with lock:
                    for group in self.groups.values():
                        for handler in group:
                            args = None

                            if isinstance(handler, handler_type):
                                try:
                                    if await handler.check(self.client, parsed_update):
                                        args = (parsed_update,)
                                except Exception as e:
                                    log.error(e, exc_info=True)
                                    continue

                            elif isinstance(handler, RawUpdateHandler):
                                args = (update, users, chats)

                            if args is None:
                                continue

                            try:
                                if inspect.iscoroutinefunction(handler.callback):
                                    await handler.callback(self.client, *args)
                                else:
                                    await self.loop.run_in_executor(
                                        self.client.executor,
                                        handler.callback,
                                        self.client,
                                        *args
                                    )
                            except gramscript.StopPropagation:
                                raise
                            except gramscript.ContinuePropagation:
                                continue
                            except Exception as e:
                                log.error(e, exc_info=True)

                            break
            except gramscript.StopPropagation:
                pass
            except Exception as e:
                log.error(e, exc_info=True)
