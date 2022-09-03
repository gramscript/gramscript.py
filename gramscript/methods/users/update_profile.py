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


class UpdateProfile(Scaffold):
    async def update_profile(
        self,
        first_name: str = None,
        last_name: str = None,
        bio: str = None
    ) -> bool:
        """Update your profile details such as first name, last name and bio.

        You can omit the parameters you don't want to change.

        Parameters:
            first_name (``str``, *optional*):
                The new first name.

            last_name (``str``, *optional*):
                The new last name.
                Pass "" (empty string) to remove it.

            bio (``str``, *optional*):
                The new bio, also known as "about". Max 70 characters.
                Pass "" (empty string) to remove it.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Update your first name only
                app.update_profile(first_name="gramscript")

                # Update first name and bio
                app.update_profile(first_name="gramscript", bio="https://docs.gramscript.org/")

                # Remove the last name
                app.update_profile(last_name="")
        """

        return bool(
            await self.send(
                raw.functions.account.UpdateProfile(
                    first_name=first_name,
                    last_name=last_name,
                    about=bio
                )
            )
        )
