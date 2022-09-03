from gramscript.scaffold import Scaffold
from gramscript import types
from typing import AsyncGenerator, Optional
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


class IterDialogs(Scaffold):
    async def iter_dialogs(
        self,
        limit: int = 0,
        offset_date: int = 0
    ) -> Optional[AsyncGenerator["types.Dialog", None]]:
        """Iterate through a user's dialogs sequentially.

        This convenience method does the same as repeatedly calling :meth:`~gramscript.Client.get_dialogs` in a loop,
        thus saving you from the hassle of setting up boilerplate code. It is useful for getting the whole dialogs list
        with a single call.

        Parameters:
            limit (``int``, *optional*):
                Limits the number of dialogs to be retrieved.
                By default, no limit is applied and all dialogs are returned.

            offset_date (``int``):
                The offset date in Unix time taken from the top message of a :obj:`~gramscript.types.Dialog`.
                Defaults to 0 (most recent dialog).

        Returns:
            ``Generator``: A generator yielding :obj:`~gramscript.types.Dialog` objects.

        Example:
            .. code-block:: python

                # Iterate through all dialogs
                for dialog in app.iter_dialogs():
                    print(dialog.chat.first_name or dialog.chat.title)
        """
        current = 0
        total = limit or (1 << 31) - 1
        limit = min(100, total)

        pinned_dialogs = await self.get_dialogs(
            pinned_only=True
        )

        for dialog in pinned_dialogs:
            yield dialog

            current += 1

            if current >= total:
                return

        while True:
            dialogs = await self.get_dialogs(
                offset_date=offset_date,
                limit=limit
            )

            if not dialogs:
                return

            offset_date = dialogs[-1].top_message.date

            for dialog in dialogs:
                yield dialog

                current += 1

                if current >= total:
                    return
