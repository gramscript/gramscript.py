from gramscript.scaffold import Scaffold
from gramscript import raw
from typing import Union, BinaryIO
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


class SetProfilePhoto(Scaffold):
    async def set_profile_photo(
        self,
        *,
        photo: Union[str, BinaryIO] = None,
        video: Union[str, BinaryIO] = None
    ) -> bool:
        """Set a new profile photo or video (H.264/MPEG-4 AVC video, max 5 seconds).

        The ``photo`` and ``video`` arguments are mutually exclusive.
        Pass either one as named argument (see examples below).

        .. note::

            This method only works for Users.
            Bots profile photos must be set using BotFather.

        Parameters:
            photo (``str`` | ``BinaryIO``, *optional*):
                Profile photo to set.
                Pass a file path as string to upload a new photo that exists on your local machine or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

            video (``str`` | ``BinaryIO``, *optional*):
                Profile video to set.
                Pass a file path as string to upload a new video that exists on your local machine or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Set a new profile photo
                app.set_profile_photo(photo="new_photo.jpg")

                # Set a new profile video
                app.set_profile_photo(video="new_video.mp4")
        """

        return bool(
            await self.send(
                raw.functions.photos.UploadProfilePhoto(
                    file=await self.save_file(photo),
                    video=await self.save_file(video)
                )
            )
        )
