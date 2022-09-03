from .vote_poll import VotePoll
from .stop_poll import StopPoll
from .send_voice import SendVoice
from .send_video_note import SendVideoNote
from .send_video import SendVideo
from .send_venue import SendVenue
from .send_sticker import SendSticker
from .send_poll import SendPoll
from .send_photo import SendPhoto
from .send_message import SendMessage
from .send_media_group import SendMediaGroup
from .send_location import SendLocation
from .send_document import SendDocument
from .send_dice import SendDice
from .send_contact import SendContact
from .send_chat_action import SendChatAction
from .send_cached_media import SendCachedMedia
from .send_audio import SendAudio
from .send_animation import SendAnimation
from .search_messages import SearchMessages
from .search_global import SearchGlobal
from .retract_vote import RetractVote
from .read_history import ReadHistory
from .iter_history import IterHistory
from .get_messages import GetMessages
from .get_history_count import GetHistoryCount
from .get_history import GetHistory
from .forward_messages import ForwardMessages
from .edit_message_text import EditMessageText
from .edit_message_reply_markup import EditMessageReplyMarkup
from .edit_message_media import EditMessageMedia
from .edit_message_caption import EditMessageCaption
from .edit_inline_text import EditInlineText
from .edit_inline_reply_markup import EditInlineReplyMarkup
from .edit_inline_media import EditInlineMedia
from .edit_inline_caption import EditInlineCaption
from .download_media import DownloadMedia
from .delete_messages import DeleteMessages
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


class Messages(
    DeleteMessages,
    EditMessageCaption,
    EditMessageReplyMarkup,
    EditMessageMedia,
    EditMessageText,
    ForwardMessages,
    GetHistory,
    GetMessages,
    SendAudio,
    SendChatAction,
    SendContact,
    SendDocument,
    SendAnimation,
    SendLocation,
    SendMediaGroup,
    SendMessage,
    SendPhoto,
    SendSticker,
    SendVenue,
    SendVideo,
    SendVideoNote,
    SendVoice,
    SendPoll,
    VotePoll,
    StopPoll,
    RetractVote,
    DownloadMedia,
    IterHistory,
    SendCachedMedia,
    GetHistoryCount,
    ReadHistory,
    EditInlineText,
    EditInlineCaption,
    EditInlineMedia,
    EditInlineReplyMarkup,
    SendDice,
    SearchMessages,
    SearchGlobal
):
    pass
