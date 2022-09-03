from gramscript.scaffold import Scaffold
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


class SignUp(Scaffold):
    async def sign_up(
        self,
        phone_number: str,
        phone_code_hash: str,
        first_name: str,
        last_name: str = ""
    ) -> "types.User":
        """Register a new user in Telegram.

        Parameters:
            phone_number (``str``):
                Phone number in international format (includes the country prefix).

            phone_code_hash (``str``):
                Code identifier taken from the result of :meth:`~gramscript.Client.send_code`.

            first_name (``str``):
                New user first name.

            last_name (``str``, *optional*):
                New user last name. Defaults to "" (empty string, no last name).

        Returns:
            :obj:`~gramscript.types.User`: On success, the new registered user is returned.

        Raises:
            BadRequest: In case the arguments are invalid.
        """
        phone_number = phone_number.strip(" +")

        r = await self.send(
            raw.functions.auth.SignUp(
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name,
                phone_code_hash=phone_code_hash
            )
        )

        await self.storage.user_id(r.user.id)
        await self.storage.is_bot(False)

        return types.User._parse(self, r.user)
