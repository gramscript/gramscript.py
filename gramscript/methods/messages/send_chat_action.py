from gramscript.scaffold import Scaffold
from gramscript import raw
from typing import Union
import json
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


class ChatAction:
    TYPING = raw.types.SendMessageTypingAction
    UPLOAD_PHOTO = raw.types.SendMessageUploadPhotoAction
    RECORD_VIDEO = raw.types.SendMessageRecordVideoAction
    UPLOAD_VIDEO = raw.types.SendMessageUploadVideoAction
    RECORD_AUDIO = raw.types.SendMessageRecordAudioAction
    UPLOAD_AUDIO = raw.types.SendMessageUploadAudioAction
    UPLOAD_DOCUMENT = raw.types.SendMessageUploadDocumentAction
    FIND_LOCATION = raw.types.SendMessageGeoLocationAction
    RECORD_VIDEO_NOTE = raw.types.SendMessageRecordRoundAction
    UPLOAD_VIDEO_NOTE = raw.types.SendMessageUploadRoundAction
    PLAYING = raw.types.SendMessageGamePlayAction
    CHOOSE_CONTACT = raw.types.SendMessageChooseContactAction
    CANCEL = raw.types.SendMessageCancelAction


POSSIBLE_VALUES = list(map(lambda x: x.lower(), filter(
    lambda x: not x.startswith("__"), ChatAction.__dict__.keys())))


class SendChatAction(Scaffold):
    async def send_chat_action(self, chat_id: Union[int, str], action: str) -> bool:
        """Tell the other party that something is happening on your side.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            action (``str``):
                Type of action to broadcast. Choose one, depending on what the user is about to receive: *"typing"* for
                text messages, *"upload_photo"* for photos, *"record_video"* or *"upload_video"* for videos,
                *"record_audio"* or *"upload_audio"* for audio files, *"upload_document"* for general files,
                *"find_location"* for location data, *"record_video_note"* or *"upload_video_note"* for video notes,
                *"choose_contact"* for contacts, *"playing"* for games or *"cancel"* to cancel any chat action currently
                displayed.

        Returns:
            ``bool``: On success, True is returned.

        Raises:
            ValueError: In case the provided string is not a valid chat action.

        Example:
            .. code-block:: python

                # Send "typing" chat action
                app.send_chat_action(chat_id, "typing")

                # Send "upload_video" chat action
                app.send_chat_action(chat_id, "upload_video")

                # Send "playing" chat action
                app.send_chat_action(chat_id, "playing")

                # Cancel any current chat action
                app.send_chat_action(chat_id, "cancel")
        """

        try:
            action = ChatAction.__dict__[action.upper()]
        except KeyError:
            raise ValueError("Invalid chat action '{}'. Possible values are: {}".format(
                action, json.dumps(POSSIBLE_VALUES, indent=4))) from None

        if "Upload" in action.__name__:
            action = action(progress=0)
        else:
            action = action()

        return await self.send(
            raw.functions.messages.SetTyping(
                peer=await self.resolve_peer(chat_id),
                action=action
            )
        )
