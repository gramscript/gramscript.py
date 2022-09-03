from gramscript.utils import compute_password_check
from gramscript.scaffold import Scaffold
from gramscript import raw
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


class RemoveCloudPassword(Scaffold):
    async def remove_cloud_password(
        self,
        password: str
    ) -> bool:
        """Turn off the Two-Step Verification security feature (Cloud Password) on your account.

        Parameters:
            password (``str``):
                Your current password.

        Returns:
            ``bool``: True on success.

        Raises:
            ValueError: In case there is no cloud password to remove.

        Example:
            .. code-block:: python

                app.remove_cloud_password("password")
        """
        r = await self.send(raw.functions.account.GetPassword())

        if not r.has_password:
            raise ValueError("There is no cloud password to remove")

        await self.send(
            raw.functions.account.UpdatePasswordSettings(
                password=compute_password_check(r, password),
                new_settings=raw.types.account.PasswordInputSettings(
                    new_algo=raw.types.PasswordKdfAlgoUnknown(),
                    new_password_hash=b"",
                    hint=""
                )
            )
        )

        return True
