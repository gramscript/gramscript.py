from gramscript.scaffold import Scaffold
from gramscript import utils
from gramscript import types
from gramscript import raw
from typing import Union
import re
import os
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


class EditMessageMedia(Scaffold):
    async def edit_message_media(
        self,
        chat_id: Union[int, str],
        message_id: int,
        media: "types.InputMedia",
        reply_markup: "types.InlineKeyboardMarkup" = None,
        file_name: str = None
    ) -> "types.Message":
        """Edit animation, audio, document, photo or video messages.

        If a message is a part of a message album, then it can be edited only to a photo or a video. Otherwise, the
        message type can be changed arbitrarily.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Message identifier in the chat specified in chat_id.

            media (:obj:`~gramscript.types.InputMedia`):
                One of the InputMedia objects describing an animation, audio, document, photo or video.

            reply_markup (:obj:`~gramscript.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

            file_name (``str``, *optional*):
                File name of the media to be sent. Not applicable to photos.
                Defaults to file's path basename.

        Returns:
            :obj:`~gramscript.types.Message`: On success, the edited message is returned.

        Example:
            .. code-block:: python

                from gramscript import InputMediaPhoto, InputMediaVideo, InputMediaAudio

                # Replace the current media with a local photo
                app.edit_message_media(chat_id, message_id, InputMediaPhoto("new_photo.jpg"))

                # Replace the current media with a local video
                app.edit_message_media(chat_id, message_id, InputMediaVideo("new_video.mp4"))

                # Replace the current media with a local audio
                app.edit_message_media(chat_id, message_id, InputMediaAudio("new_audio.mp3"))
        """
        caption = media.caption
        parse_mode = media.parse_mode

        if isinstance(media, types.InputMediaPhoto):
            if os.path.isfile(media.media):
                media = await self.send(
                    raw.functions.messages.UploadMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=raw.types.InputMediaUploadedPhoto(
                            file=await self.save_file(media.media)
                        )
                    )
                )

                media = raw.types.InputMediaPhoto(
                    id=raw.types.InputPhoto(
                        id=media.photo.id,
                        access_hash=media.photo.access_hash,
                        file_reference=media.photo.file_reference
                    )
                )
            elif re.match("^https?://", media.media):
                media = raw.types.InputMediaPhotoExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(
                    media.media, media.file_ref, 2)
        elif isinstance(media, types.InputMediaVideo):
            if os.path.isfile(media.media):
                media = await self.send(
                    raw.functions.messages.UploadMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=raw.types.InputMediaUploadedDocument(
                            mime_type=self.guess_mime_type(
                                media.media) or "video/mp4",
                            thumb=await self.save_file(media.thumb),
                            file=await self.save_file(media.media),
                            attributes=[
                                raw.types.DocumentAttributeVideo(
                                    supports_streaming=media.supports_streaming or None,
                                    duration=media.duration,
                                    w=media.width,
                                    h=media.height
                                ),
                                raw.types.DocumentAttributeFilename(
                                    file_name=file_name or os.path.basename(
                                        media.media)
                                )
                            ]
                        )
                    )
                )

                media = raw.types.InputMediaDocument(
                    id=raw.types.InputDocument(
                        id=media.document.id,
                        access_hash=media.document.access_hash,
                        file_reference=media.document.file_reference
                    )
                )
            elif re.match("^https?://", media.media):
                media = raw.types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(
                    media.media, media.file_ref, 4)
        elif isinstance(media, types.InputMediaAudio):
            if os.path.isfile(media.media):
                media = await self.send(
                    raw.functions.messages.UploadMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=raw.types.InputMediaUploadedDocument(
                            mime_type=self.guess_mime_type(
                                media.media) or "audio/mpeg",
                            thumb=await self.save_file(media.thumb),
                            file=await self.save_file(media.media),
                            attributes=[
                                raw.types.DocumentAttributeAudio(
                                    duration=media.duration,
                                    performer=media.performer,
                                    title=media.title
                                ),
                                raw.types.DocumentAttributeFilename(
                                    file_name=file_name or os.path.basename(
                                        media.media)
                                )
                            ]
                        )
                    )
                )

                media = raw.types.InputMediaDocument(
                    id=raw.types.InputDocument(
                        id=media.document.id,
                        access_hash=media.document.access_hash,
                        file_reference=media.document.file_reference
                    )
                )
            elif re.match("^https?://", media.media):
                media = raw.types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(
                    media.media, media.file_ref, 9)
        elif isinstance(media, types.InputMediaAnimation):
            if os.path.isfile(media.media):
                media = await self.send(
                    raw.functions.messages.UploadMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=raw.types.InputMediaUploadedDocument(
                            mime_type=self.guess_mime_type(
                                media.media) or "video/mp4",
                            thumb=await self.save_file(media.thumb),
                            file=await self.save_file(media.media),
                            attributes=[
                                raw.types.DocumentAttributeVideo(
                                    supports_streaming=True,
                                    duration=media.duration,
                                    w=media.width,
                                    h=media.height
                                ),
                                raw.types.DocumentAttributeFilename(
                                    file_name=file_name or os.path.basename(
                                        media.media)
                                ),
                                raw.types.DocumentAttributeAnimated()
                            ]
                        )
                    )
                )

                media = raw.types.InputMediaDocument(
                    id=raw.types.InputDocument(
                        id=media.document.id,
                        access_hash=media.document.access_hash,
                        file_reference=media.document.file_reference
                    )
                )
            elif re.match("^https?://", media.media):
                media = raw.types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(
                    media.media, media.file_ref, 10)
        elif isinstance(media, types.InputMediaDocument):
            if os.path.isfile(media.media):
                media = await self.send(
                    raw.functions.messages.UploadMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=raw.types.InputMediaUploadedDocument(
                            mime_type=self.guess_mime_type(
                                media.media) or "application/zip",
                            thumb=await self.save_file(media.thumb),
                            file=await self.save_file(media.media),
                            attributes=[
                                raw.types.DocumentAttributeFilename(
                                    file_name=file_name or os.path.basename(
                                        media.media)
                                )
                            ]
                        )
                    )
                )

                media = raw.types.InputMediaDocument(
                    id=raw.types.InputDocument(
                        id=media.document.id,
                        access_hash=media.document.access_hash,
                        file_reference=media.document.file_reference
                    )
                )
            elif re.match("^https?://", media.media):
                media = raw.types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(
                    media.media, media.file_ref, 5)

        r = await self.send(
            raw.functions.messages.EditMessage(
                peer=await self.resolve_peer(chat_id),
                id=message_id,
                media=media,
                reply_markup=reply_markup.write() if reply_markup else None,
                **await self.parser.parse(caption, parse_mode)
            )
        )

        for i in r.updates:
            if isinstance(i, (raw.types.UpdateEditMessage, raw.types.UpdateEditChannelMessage)):
                return await types.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats}
                )
