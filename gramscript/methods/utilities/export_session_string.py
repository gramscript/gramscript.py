from gramscript.scaffold import Scaffold
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


class ExportSessionString(Scaffold):
    async def export_session_string(self):
        """Export the current authorized session as a serialized string.

        Session strings are useful for storing in-memory authorized sessions in a portable, serialized string.
        More detailed information about session strings can be found at the dedicated page of
        :doc:`Storage Engines <../../topics/storage-engines>`.

        Returns:
            ``str``: The session serialized into a printable, url-safe string.

        Example:
            .. code-block:: python
                :emphasize-lines: 6

                from gramscript import Client

                app = Client("my_account")

                with app:
                    print(app.export_session_string())
        """
        return await self.storage.export_session_string()
