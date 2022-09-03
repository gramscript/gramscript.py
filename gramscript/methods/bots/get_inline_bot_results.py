from gramscript.scaffold import Scaffold
from gramscript.errors import UnknownError
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


class GetInlineBotResults(Scaffold):
    async def get_inline_bot_results(
        self,
        bot: Union[int, str],
        query: str = "",
        offset: str = "",
        latitude: float = None,
        longitude: float = None
    ):
        """Get bot results via inline queries.
        You can then send a result using :meth:`~gramscript.Client.send_inline_bot_result`

        Parameters:
            bot (``int`` | ``str``):
                Unique identifier of the inline bot you want to get results from. You can specify
                a @username (str) or a bot ID (int).

            query (``str``, *optional*):
                Text of the query (up to 512 characters).
                Defaults to "" (empty string).

            offset (``str``, *optional*):
                Offset of the results to be returned.

            latitude (``float``, *optional*):
                Latitude of the location.
                Useful for location-based results only.

            longitude (``float``, *optional*):
                Longitude of the location.
                Useful for location-based results only.

        Returns:
            :obj:`BotResults <gramscript.api.types.messages.BotResults>`: On Success.

        Raises:
            TimeoutError: In case the bot fails to answer within 10 seconds.

        Example:
            .. code-block:: python

                results = app.get_inline_bot_results("gramscriptbot")
                print(results)
        """
        # TODO: Don't return the raw type

        try:
            return await self.send(
                raw.functions.messages.GetInlineBotResults(
                    bot=await self.resolve_peer(bot),
                    peer=raw.types.InputPeerSelf(),
                    query=query,
                    offset=offset,
                    geo_point=raw.types.InputGeoPoint(
                        lat=latitude,
                        long=longitude
                    ) if (latitude is not None and longitude is not None) else None
                )
            )
        except UnknownError as e:
            # TODO: Add this -503 Timeout error into the Error DB
            if e.x.error_code == -503 and e.x.error_message == "Timeout":
                raise TimeoutError(
                    "The inline bot didn't answer in time") from None
            else:
                raise e
