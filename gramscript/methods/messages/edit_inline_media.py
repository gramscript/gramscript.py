from .inline_session import get_session
from gramscript.scaffold import Scaffold
from gramscript import utils
from gramscript import types
from gramscript import raw
import re
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


class EditInlineMedia(Scaffold):
    async def edit_inline_media(
        self,
        inline_message_id: str,
        media: "types.InputMedia",
        reply_markup: "types.InlineKeyboardMarkup" = None
    ) -> bool:
        """Edit inline animation, audio, document, photo or video messages.

        When the inline message is edited, a new file can't be uploaded. Use a previously uploaded file via its file_id
        or specify a URL.

        Parameters:
            inline_message_id (``str``):
                Required if *chat_id* and *message_id* are not specified.
                Identifier of the inline message.

            media (:obj:`~gramscript.types.InputMedia`):
                One of the InputMedia objects describing an animation, audio, document, photo or video.

            reply_markup (:obj:`~gramscript.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                from gramscript import InputMediaPhoto, InputMediaVideo, InputMediaAudio

                # Bots only

                # Replace the current media with a local photo
                app.edit_inline_media(inline_message_id, InputMediaPhoto("new_photo.jpg"))

                # Replace the current media with a local video
                app.edit_inline_media(inline_message_id, InputMediaVideo("new_video.mp4"))

                # Replace the current media with a local audio
                app.edit_inline_media(inline_message_id, InputMediaAudio("new_audio.mp3"))
        """
        caption = media.caption
        parse_mode = media.parse_mode

        if isinstance(media, types.InputMediaPhoto):
            if re.match("^https?://", media.media):
                media = raw.types.InputMediaPhotoExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(
                    media.media, media.file_ref, 2)
        elif isinstance(media, types.InputMediaVideo):
            if re.match("^https?://", media.media):
                media = raw.types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(
                    media.media, media.file_ref, 4)
        elif isinstance(media, types.InputMediaAudio):
            if re.match("^https?://", media.media):
                media = raw.types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(
                    media.media, media.file_ref, 9)
        elif isinstance(media, types.InputMediaAnimation):
            if re.match("^https?://", media.media):
                media = raw.types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(
                    media.media, media.file_ref, 10)
        elif isinstance(media, types.InputMediaDocument):
            if re.match("^https?://", media.media):
                media = raw.types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(
                    media.media, media.file_ref, 5)

        unpacked = utils.unpack_inline_message_id(inline_message_id)
        dc_id = unpacked.dc_id

        session = get_session(self, dc_id)

        return await session.send(
            raw.functions.messages.EditInlineBotMessage(
                id=unpacked,
                media=media,
                reply_markup=reply_markup.write() if reply_markup else None,
                **await self.parser.parse(caption, parse_mode)
            )
        )
