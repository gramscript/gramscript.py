from gramscript.scaffold import Scaffold
from gramscript import types
from gramscript import raw
from typing import Union
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


class SendMessage(Scaffold):
    async def send_message(
        self,
        chat_id: Union[int, str],
        text: str,
        parse_mode: Union[str, None] = object,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        schedule_date: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "types.Message":
        """Send text messages.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            text (``str``):
                Text of the message to be sent.

            parse_mode (``str``, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.
                Pass "markdown" or "md" to enable Markdown-style parsing only.
                Pass "html" to enable HTML-style parsing only.
                Pass None to completely disable style parsing.

            disable_web_page_preview (``bool``, *optional*):
                Disables link previews for links in this message.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            schedule_date (``int``, *optional*):
                Date when the message will be automatically sent. Unix time.

            reply_markup (:obj:`~gramscript.types.InlineKeyboardMarkup` | :obj:`~gramscript.types.ReplyKeyboardMarkup` | :obj:`~gramscript.types.ReplyKeyboardRemove` | :obj:`~gramscript.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            :obj:`~gramscript.types.Message`: On success, the sent text message is returned.

        Example:
            .. code-block:: python
                :emphasize-lines: 2,5,8,11,21-23,26-32

                # Simple example
                app.send_message("haskell", "Thanks for creating **gramscript**!")

                # Disable web page previews
                app.send_message("me", "https://docs.gramscript.org", disable_web_page_preview=True)

                # Reply to a message using its id
                app.send_message("me", "this is a reply", reply_to_message_id=12345)

                # Force HTML-only styles for this request only
                app.send_message("me", "**not bold**, <i>italic<i>", parse_mode="html")

                ##
                # For bots only, send messages with keyboards attached
                ##

                from gramscript import (
                    ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton)

                # Send a normal keyboard
                app.send_message(
                    chat_id, "Look at that button!",
                    reply_markup=ReplyKeyboardMarkup([["Nice!"]]))

                # Send an inline keyboard
                app.send_message(
                    chat_id, "These are inline buttons",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton("Data", callback_data="hidden_callback_data")],
                            [InlineKeyboardButton("Docs", url="https://docs.gramscript.org")]
                        ]))
        """

        message, entities = (await self.parser.parse(text, parse_mode)).values()

        r = await self.send(
            raw.functions.messages.SendMessage(
                peer=await self.resolve_peer(chat_id),
                no_webpage=disable_web_page_preview or None,
                silent=disable_notification or None,
                reply_to_msg_id=reply_to_message_id,
                random_id=self.rnd_id(),
                schedule_date=schedule_date,
                reply_markup=reply_markup.write() if reply_markup else None,
                message=message,
                entities=entities
            )
        )

        if isinstance(r, raw.types.UpdateShortSentMessage):
            peer = await self.resolve_peer(chat_id)

            peer_id = (
                peer.user_id
                if isinstance(peer, raw.types.InputPeerUser)
                else -peer.chat_id
            )

            return types.Message(
                message_id=r.id,
                chat=types.Chat(
                    id=peer_id,
                    type="private",
                    client=self
                ),
                text=message,
                date=r.date,
                outgoing=r.out,
                entities=[
                    types.MessageEntity._parse(None, entity, {})
                    for entity in entities
                ],
                client=self
            )

        for i in r.updates:
            if isinstance(i, (raw.types.UpdateNewMessage,
                              raw.types.UpdateNewChannelMessage,
                              raw.types.UpdateNewScheduledMessage)):
                return await types.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    is_scheduled=isinstance(
                        i, raw.types.UpdateNewScheduledMessage)
                )
