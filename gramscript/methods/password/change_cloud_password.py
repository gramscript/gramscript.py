from gramscript.utils import compute_password_hash, compute_password_check, btoi, itob
from gramscript.scaffold import Scaffold
from gramscript import raw
import os
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


class ChangeCloudPassword(Scaffold):
    async def change_cloud_password(
        self,
        current_password: str,
        new_password: str,
        new_hint: str = ""
    ) -> bool:
        """Change your Two-Step Verification password (Cloud Password) with a new one.

        Parameters:
            current_password (``str``):
                Your current password.

            new_password (``str``):
                Your new password.

            new_hint (``str``, *optional*):
                A new password hint.

        Returns:
            ``bool``: True on success.

        Raises:
            ValueError: In case there is no cloud password to change.

        Example:
            .. code-block:: python

                # Change password only
                app.change_cloud_password("current_password", "new_password")

                # Change password and hint
                app.change_cloud_password("current_password", "new_password", new_hint="hint")
        """
        r = await self.send(raw.functions.account.GetPassword())

        if not r.has_password:
            raise ValueError("There is no cloud password to change")

        r.new_algo.salt1 += os.urandom(32)
        new_hash = btoi(compute_password_hash(r.new_algo, new_password))
        new_hash = itob(pow(r.new_algo.g, new_hash, btoi(r.new_algo.p)))

        await self.send(
            raw.functions.account.UpdatePasswordSettings(
                password=compute_password_check(r, current_password),
                new_settings=raw.types.account.PasswordInputSettings(
                    new_algo=r.new_algo,
                    new_password_hash=new_hash,
                    hint=new_hint
                )
            )
        )

        return True
