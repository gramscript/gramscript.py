from gramscript.scaffold import Scaffold
from gramscript import types
from gramscript import raw
from typing import Iterable, Union, List
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


class GetUsers(Scaffold):
    async def get_users(
        self,
        user_ids: Union[Iterable[Union[int, str]], int, str]
    ) -> Union["types.User", List["types.User"]]:
        """Get information about a user.
        You can retrieve up to 200 users at once.

        Parameters:
            user_ids (``iterable``):
                A list of User identifiers (id or username) or a single user id/username.
                For a contact that exists in your Telegram address book you can use his phone number (str).
                Iterators and Generators are also accepted.

        Returns:
            :obj:`~gramscript.types.User` | List of :obj:`~gramscript.types.User`: In case *user_ids* was an integer or
            string the single requested user is returned, otherwise, in case *user_ids* was an iterable a list of users
            is returned, even if the iterable contained one item only.

        Example:
            .. code-block:: python

                # Get information about one user
                app.get_users("haskell")

                # Get information about multiple users at once
                app.get_users([user1, user2, user3])
        """
        is_iterable = not isinstance(user_ids, (int, str))
        user_ids = list(user_ids) if is_iterable else [user_ids]
        user_ids = await asyncio.gather(*[self.resolve_peer(i) for i in user_ids])

        r = await self.send(
            raw.functions.users.GetUsers(
                id=user_ids
            )
        )

        users = types.List()

        for i in r:
            users.append(types.User._parse(self, i))

        return users if is_iterable else users[0]
