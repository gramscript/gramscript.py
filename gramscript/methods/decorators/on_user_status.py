from gramscript.scaffold import Scaffold
from gramscript.filters import Filter
import gramscript
from typing import Callable
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


class OnUserStatus(Scaffold):
    def on_user_status(
        self=None,
        filters=None,
        group: int = 0
    ) -> callable:
        """Decorator for handling user status updates.
        This does the same thing as :meth:`~gramscript.Client.add_handler` using the
        :obj:`~gramscript.handlers.UserStatusHandler`.

        Parameters:
            filters (:obj:`~gramscript.Filters`, *optional*):
                Pass one or more filters to allow only a subset of UserStatus updated to be passed in your function.

            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """

        def decorator(func: Callable) -> Callable:
            if isinstance(self, gramscript.Client):
                self.add_handler(
                    gramscript.handlers.UserStatusHandler(func, filters), group)
            elif isinstance(self, Filter) or self is None:
                func.handler = (
                    gramscript.handlers.UserStatusHandler(func, self),
                    group if filters is None else filters
                )

            return func

        return decorator
