from gramscript.scaffold import Scaffold
import gramscript
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


class StopTransmission(Scaffold):
    def stop_transmission(self):
        """Stop downloading or uploading a file.

        This method must be called inside a progress callback function in order to stop the transmission at the
        desired time. The progress callback is called every time a file chunk is uploaded/downloaded.

        Example:
            .. code-block:: python
                :emphasize-lines: 9

                from gramscript import Client

                app = Client("my_account")

                # Example to stop transmission once the upload progress reaches 50%
                # Useless in practice, but shows how to stop on command
                def progress(current, total, client):
                    if (current * 100 / total) > 50:
                        client.stop_transmission()

                with app:
                    app.send_document("me", "files.zip", progress=progress, progress_args=(app,))
        """
        raise gramscript.StopTransmission
