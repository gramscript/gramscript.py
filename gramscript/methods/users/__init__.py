from .update_username import UpdateUsername
from .update_profile import UpdateProfile
from .unblock_user import UnblockUser
from .set_profile_photo import SetProfilePhoto
from .iter_profile_photos import IterProfilePhotos
from .get_users import GetUsers
from .get_profile_photos_count import GetProfilePhotosCount
from .get_profile_photos import GetProfilePhotos
from .get_me import GetMe
from .get_common_chats import GetCommonChats
from .delete_profile_photos import DeleteProfilePhotos
from .block_user import BlockUser
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


class Users(
    BlockUser,
    GetCommonChats,
    GetProfilePhotos,
    SetProfilePhoto,
    DeleteProfilePhotos,
    GetUsers,
    GetMe,
    UpdateUsername,
    GetProfilePhotosCount,
    IterProfilePhotos,
    UnblockUser,
    UpdateProfile,
):
    pass
