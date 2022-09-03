from gramscript.scaffold import Scaffold
from gramscript import utils
from gramscript import raw
from typing import List, Union
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


class DeleteProfilePhotos(Scaffold):
    async def delete_profile_photos(
        self,
        photo_ids: Union[str, List[str]]
    ) -> bool:
        """Delete your own profile photos.

        Parameters:
            photo_ids (``str`` | List of ``str``):
                A single :obj:`~gramscript.types.Photo` id as string or multiple ids as list of strings for deleting
                more than one photos at once.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Get the photos to be deleted
                photos = app.get_profile_photos("me")

                # Delete one photo
                app.delete_profile_photos(photos[0].file_id)

                # Delete the rest of the photos
                app.delete_profile_photos([p.file_id for p in photos[1:]])
        """
        photo_ids = photo_ids if isinstance(photo_ids, list) else [photo_ids]
        input_photos = [utils.get_input_media_from_file_id(
            i).id for i in photo_ids]

        return bool(await self.send(
            raw.functions.photos.DeletePhotos(
                id=input_photos
            )
        ))
