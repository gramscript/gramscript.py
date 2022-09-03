from ... import utils
from ..update import Update
from ..object import Object
from gramscript import types
from gramscript import raw
import gramscript
from typing import Union, List, Match
from struct import pack
from base64 import b64encode
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


class CallbackQuery(Object, Update):
    """An incoming callback query from a callback button in an inline keyboard.

    If the button that originated the query was attached to a message sent by the bot, the field *message*
    will be present. If the button was attached to a message sent via the bot (in inline mode), the field
    *inline_message_id* will be present. Exactly one of the fields *data* or *game_short_name* will be present.

    Parameters:
        id (``str``):
            Unique identifier for this query.

        from_user (:obj:`~gramscript.types.User`):
            Sender.

        chat_instance (``str``, *optional*):
            Global identifier, uniquely corresponding to the chat to which the message with the callback button was
            sent. Useful for high scores in games.

        message (:obj:`~gramscript.types.Message`, *optional*):
            Message with the callback button that originated the query. Note that message content and message date will
            not be available if the message is too old.

        inline_message_id (``str``):
            Identifier of the message sent via the bot in inline mode, that originated the query.

        data (``str`` | ``bytes``, *optional*):
            Data associated with the callback button. Be aware that a bad client can send arbitrary data in this field.

        game_short_name (``str``, *optional*):
            Short name of a Game to be returned, serves as the unique identifier for the game.

        matches (List of regex Matches, *optional*):
            A list containing all `Match Objects <https://docs.python.org/3/library/re.html#match-objects>`_ that match
            the data of this callback query. Only applicable when using :obj:`Filters.regex <gramscript.Filters.regex>`.
    """

    def __init__(
        self,
        *,
        client: "gramscript.Client" = None,
        id: str,
        from_user: "types.User",
        chat_instance: str,
        message: "types.Message" = None,
        inline_message_id: str = None,
        data: Union[str, bytes] = None,
        game_short_name: str = None,
        matches: List[Match] = None
    ):
        super().__init__(client)

        self.id = id
        self.from_user = from_user
        self.chat_instance = chat_instance
        self.message = message
        self.inline_message_id = inline_message_id
        self.data = data
        self.game_short_name = game_short_name
        self.matches = matches

    @staticmethod
    async def _parse(client, callback_query, users) -> "CallbackQuery":
        message = None
        inline_message_id = None

        if isinstance(callback_query, raw.types.UpdateBotCallbackQuery):
            message = await client.get_messages(utils.get_peer_id(callback_query.peer), callback_query.msg_id)
        elif isinstance(callback_query, raw.types.UpdateInlineBotCallbackQuery):
            inline_message_id = b64encode(
                pack(
                    "<iqq",
                    callback_query.msg_id.dc_id,
                    callback_query.msg_id.id,
                    callback_query.msg_id.access_hash
                ),
                b"-_"
            ).decode().rstrip("=")

        # Try to decode callback query data into string. If that fails, fallback to bytes instead of decoding by
        # ignoring/replacing errors, this way, button clicks will still work.
        try:
            data = callback_query.data.decode()
        except UnicodeDecodeError:
            data = callback_query.data

        return CallbackQuery(
            id=str(callback_query.query_id),
            from_user=types.User._parse(client, users[callback_query.user_id]),
            message=message,
            inline_message_id=inline_message_id,
            chat_instance=str(callback_query.chat_instance),
            data=data,
            game_short_name=callback_query.game_short_name,
            client=client
        )

    async def answer(self, text: str = None, show_alert: bool = None, url: str = None, cache_time: int = 0):
        """Bound method *answer* of :obj:`~gramscript.types.CallbackQuery`.

        Use this method as a shortcut for:

        .. code-block:: python

            client.answer_callback_query(
                callback_query.id,
                text="Hello",
                show_alert=True
            )

        Example:
            .. code-block:: python

                callback_query.answer("Hello", show_alert=True)

        Parameters:
            text (``str``, *optional*):
                Text of the notification. If not specified, nothing will be shown to the user, 0-200 characters.

            show_alert (``bool`` *optional*):
                If true, an alert will be shown by the client instead of a notification at the top of the chat screen.
                Defaults to False.

            url (``str`` *optional*):
                URL that will be opened by the user's client.
                If you have created a Game and accepted the conditions via @Botfather, specify the URL that opens your
                game – note that this will only work if the query comes from a callback_game button.
                Otherwise, you may use links like t.me/your_bot?start=XXXX that open your bot with a parameter.

            cache_time (``int`` *optional*):
                The maximum amount of time in seconds that the result of the callback query may be cached client-side.
                Telegram apps will support caching starting in version 3.14. Defaults to 0.
        """
        return await self._client.answer_callback_query(
            callback_query_id=self.id,
            text=text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time
        )

    async def edit_message_text(
        self,
        text: str,
        parse_mode: Union[str, None] = object,
        disable_web_page_preview: bool = None,
        reply_markup: "types.InlineKeyboardMarkup" = None
    ) -> Union["types.Message", bool]:
        """Edit the text of messages attached to callback queries.

        Bound method *edit_message_text* of :obj:`~gramscript.types.CallbackQuery`.

        Parameters:
            text (``str``):
                New text of the message.

            parse_mode (``str``, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.
                Pass "markdown" or "md" to enable Markdown-style parsing only.
                Pass "html" to enable HTML-style parsing only.
                Pass None to completely disable style parsing.

            disable_web_page_preview (``bool``, *optional*):
                Disables link previews for links in this message.

            reply_markup (:obj:`~gramscript.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            :obj:`~gramscript.types.Message` | ``bool``: On success, if the edited message was sent by the bot, the edited
            message is returned, otherwise True is returned (message sent via the bot, as inline query result).

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if self.inline_message_id is None:
            return await self._client.edit_message_text(
                chat_id=self.message.chat.id,
                message_id=self.message.message_id,
                text=text,
                parse_mode=parse_mode,
                disable_web_page_preview=disable_web_page_preview,
                reply_markup=reply_markup
            )
        else:
            return await self._client.edit_inline_text(
                inline_message_id=self.inline_message_id,
                text=text,
                parse_mode=parse_mode,
                disable_web_page_preview=disable_web_page_preview,
                reply_markup=reply_markup
            )

    async def edit_message_caption(
        self,
        caption: str,
        parse_mode: Union[str, None] = object,
        reply_markup: "types.InlineKeyboardMarkup" = None
    ) -> Union["types.Message", bool]:
        """Edit the caption of media messages attached to callback queries.

        Bound method *edit_message_caption* of :obj:`~gramscript.types.CallbackQuery`.

        Parameters:
            caption (``str``):
                New caption of the message.

            parse_mode (``str``, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.
                Pass "markdown" or "md" to enable Markdown-style parsing only.
                Pass "html" to enable HTML-style parsing only.
                Pass None to completely disable style parsing.

            reply_markup (:obj:`~gramscript.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            :obj:`~gramscript.types.Message` | ``bool``: On success, if the edited message was sent by the bot, the edited
            message is returned, otherwise True is returned (message sent via the bot, as inline query result).

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self.edit_message_text(caption, parse_mode, reply_markup)

    async def edit_message_media(
        self,
        media: "types.InputMedia",
        reply_markup: "types.InlineKeyboardMarkup" = None
    ) -> Union["types.Message", bool]:
        """Edit animation, audio, document, photo or video messages attached to callback queries.

        Bound method *edit_message_media* of :obj:`~gramscript.types.CallbackQuery`.

        Parameters:
            media (:obj:`~gramscript.types.InputMedia`):
                One of the InputMedia objects describing an animation, audio, document, photo or video.

            reply_markup (:obj:`~gramscript.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            :obj:`~gramscript.types.Message` | ``bool``: On success, if the edited message was sent by the bot, the edited
            message is returned, otherwise True is returned (message sent via the bot, as inline query result).

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if self.inline_message_id is None:
            return await self._client.edit_message_media(
                chat_id=self.message.chat.id,
                message_id=self.message.message_id,
                media=media,
                reply_markup=reply_markup
            )
        else:
            return await self._client.edit_inline_media(
                inline_message_id=self.inline_message_id,
                media=media,
                reply_markup=reply_markup
            )

    async def edit_message_reply_markup(
        self,
        reply_markup: "types.InlineKeyboardMarkup" = None
    ) -> Union["types.Message", bool]:
        """Edit only the reply markup of messages attached to callback queries.

        Bound method *edit_message_reply_markup* of :obj:`~gramscript.types.CallbackQuery`.

        Parameters:
            reply_markup (:obj:`~gramscript.types.InlineKeyboardMarkup`):
                An InlineKeyboardMarkup object.

        Returns:
            :obj:`~gramscript.types.Message` | ``bool``: On success, if the edited message was sent by the bot, the edited
            message is returned, otherwise True is returned (message sent via the bot, as inline query result).

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if self.inline_message_id is None:
            return await self._client.edit_message_reply_markup(
                chat_id=self.message.chat.id,
                message_id=self.message.message_id,
                reply_markup=reply_markup
            )
        else:
            return await self._client.edit_inline_reply_markup(
                inline_message_id=self.inline_message_id,
                reply_markup=reply_markup
            )
