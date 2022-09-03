from gramscript.session import Session, Auth
from gramscript.scaffold import Scaffold
from gramscript.errors import PhoneMigrate, NetworkMigrate
from gramscript import types
from gramscript import raw
import logging
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


class SendCode(Scaffold):
    async def send_code(self, phone_number: str) -> "types.SentCode":
        """Send the confirmation code to the given phone number.

        Parameters:
            phone_number (``str``):
                Phone number in international format (includes the country prefix).

        Returns:
            :obj:`~gramscript.types.SentCode`: On success, an object containing information on the sent confirmation code
            is returned.

        Raises:
            BadRequest: In case the phone number is invalid.
        """
        phone_number = phone_number.strip(" +")

        while True:
            try:
                r = await self.send(
                    raw.functions.auth.SendCode(
                        phone_number=phone_number,
                        api_id=self.api_id,
                        api_hash=self.api_hash,
                        settings=raw.types.CodeSettings()
                    )
                )
            except (PhoneMigrate, NetworkMigrate) as e:
                await self.session.stop()

                await self.storage.dc_id(e.x)
                await self.storage.auth_key(
                    await Auth(
                        self, await self.storage.dc_id(),
                        await self.storage.test_mode()
                    ).create()
                )
                self.session = Session(
                    self, await self.storage.dc_id(),
                    await self.storage.auth_key(), await self.storage.test_mode()
                )

                await self.session.start()
            else:
                return types.SentCode._parse(r)
