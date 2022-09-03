from .update_chat_username import UpdateChatUsername
from .unpin_chat_message import UnpinChatMessage
from .unban_chat_member import UnbanChatMember
from .unarchive_chats import UnarchiveChats
from .set_slow_mode import SetSlowMode
from .set_chat_title import SetChatTitle
from .set_chat_photo import SetChatPhoto
from .set_chat_permissions import SetChatPermissions
from .set_chat_description import SetChatDescription
from .set_administrator_title import SetAdministratorTitle
from .restrict_chat_member import RestrictChatMember
from .promote_chat_member import PromoteChatMember
from .pin_chat_message import PinChatMessage
from .leave_chat import LeaveChat
from .kick_chat_member import KickChatMember
from .join_chat import JoinChat
from .iter_dialogs import IterDialogs
from .iter_chat_members import IterChatMembers
from .get_nearby_chats import GetNearbyChats
from .get_dialogs_count import GetDialogsCount
from .get_dialogs import GetDialogs
from .get_chat_members_count import GetChatMembersCount
from .get_chat_members import GetChatMembers
from .get_chat_member import GetChatMember
from .get_chat import GetChat
from .export_chat_invite_link import ExportChatInviteLink
from .delete_supergroup import DeleteSupergroup
from .delete_chat_photo import DeleteChatPhoto
from .delete_channel import DeleteChannel
from .create_supergroup import CreateSupergroup
from .create_group import CreateGroup
from .create_channel import CreateChannel
from .archive_chats import ArchiveChats
from .add_chat_members import AddChatMembers
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


class Chats(
    GetChat,
    ExportChatInviteLink,
    LeaveChat,
    JoinChat,
    KickChatMember,
    UnbanChatMember,
    RestrictChatMember,
    PromoteChatMember,
    GetChatMembers,
    GetChatMember,
    SetChatPhoto,
    DeleteChatPhoto,
    SetChatTitle,
    SetChatDescription,
    PinChatMessage,
    UnpinChatMessage,
    GetDialogs,
    GetChatMembersCount,
    IterDialogs,
    IterChatMembers,
    UpdateChatUsername,
    SetChatPermissions,
    GetDialogsCount,
    ArchiveChats,
    UnarchiveChats,
    CreateGroup,
    CreateSupergroup,
    CreateChannel,
    AddChatMembers,
    DeleteChannel,
    DeleteSupergroup,
    GetNearbyChats,
    SetAdministratorTitle,
    SetSlowMode
):
    pass
