from ..update import Update
from ..object import Object
from gramscript import types
from gramscript import raw
import gramscript
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


class ChosenInlineResult(Object, Update):
    """A :doc:`result <InlineQueryResult>` of an inline query chosen by the user and sent to their chat partner.

    Parameters:
        result_id (``str``):
            The unique identifier for the result that was chosen.

        from_user (:obj:`~gramscript.types.User`):
            The user that chose the result.

        query (``str``):
            The query that was used to obtain the result.

        location (:obj:`~gramscript.types.Location`, *optional*):
            Sender location, only for bots that require user location.

        inline_message_id (``str``, *optional*):
            Identifier of the sent inline message.
            Available only if there is an :doc:`inline keyboard <InlineKeyboardMarkup>` attached to the message.
            Will be also received in :doc:`callback queries <CallbackQuery>` and can be used to edit the message.

    .. note::

        It is necessary to enable inline feedback via `@Botfather <https://t.me/botfather>`_ in order to receive these
        objects in updates.
    """

    def __init__(
        self,
        *,
        client: "gramscript.Client" = None,
        result_id: str,
        from_user: "types.User",
        query: str,
        location: "types.Location" = None,
        inline_message_id: str = None
    ):
        super().__init__(client)

        self.result_id = result_id
        self.from_user = from_user
        self.query = query
        self.location = location
        self.inline_message_id = inline_message_id

    @staticmethod
    def _parse(client, chosen_inline_result: raw.types.UpdateBotInlineSend, users) -> "ChosenInlineResult":
        inline_message_id = None

        if isinstance(chosen_inline_result.msg_id, raw.types.InputBotInlineMessageID):
            inline_message_id = b64encode(
                pack(
                    "<iqq",
                    chosen_inline_result.msg_id.dc_id,
                    chosen_inline_result.msg_id.id,
                    chosen_inline_result.msg_id.access_hash
                ),
                b"-_"
            ).decode().rstrip("=")

        return ChosenInlineResult(
            result_id=str(chosen_inline_result.id),
            from_user=types.User._parse(
                client, users[chosen_inline_result.user_id]),
            query=chosen_inline_result.query,
            location=types.Location(
                longitude=chosen_inline_result.geo.long,
                latitude=chosen_inline_result.geo.lat,
                client=client
            ) if chosen_inline_result.geo else None,
            inline_message_id=inline_message_id
        )
