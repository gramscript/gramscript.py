from gramscript.scaffold import Scaffold
from gramscript import utils
from gramscript import types
from gramscript import raw
from typing import Union, List
import re
import os
import logging
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


log = logging.getLogger(__name__)


class SendMediaGroup(Scaffold):
    # TODO: Add progress parameter
    async def send_media_group(
        self,
        chat_id: Union[int, str],
        media: List[Union["types.InputMediaPhoto", "types.InputMediaVideo"]],
        disable_notification: bool = None,
        reply_to_message_id: int = None
    ) -> List["types.Message"]:
        """Send a group of photos or videos as an album.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            media (List of :obj:`~gramscript.types.InputMediaPhoto` and :obj:`~gramscript.types.InputMediaVideo`):
                A list describing photos and videos to be sent, must include 2–10 items.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

        Returns:
            List of :obj:`~gramscript.types.Message`: On success, a list of the sent messages is returned.

        Example:
            .. code-block:: python

                from gramscript import InputMediaPhoto, InputMediaVideo

                app.send_media_group(
                    "me",
                    [
                        InputMediaPhoto("photo1.jpg"),
                        InputMediaPhoto("photo2.jpg", caption="photo caption"),
                        InputMediaVideo("video.mp4", caption="a video")
                    ]
                )
        """
        multi_media = []

        for i in media:
            if isinstance(i, types.InputMediaPhoto):
                if os.path.isfile(i.media):
                    media = await self.send(
                        raw.functions.messages.UploadMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=raw.types.InputMediaUploadedPhoto(
                                file=await self.save_file(i.media)
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
                elif re.match("^https?://", i.media):
                    media = await self.send(
                        raw.functions.messages.UploadMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=raw.types.InputMediaPhotoExternal(
                                url=i.media
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
                else:
                    media = utils.get_input_media_from_file_id(
                        i.media, i.file_ref, 2)
            elif isinstance(i, types.InputMediaVideo):
                if os.path.isfile(i.media):
                    media = await self.send(
                        raw.functions.messages.UploadMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=raw.types.InputMediaUploadedDocument(
                                file=await self.save_file(i.media),
                                thumb=await self.save_file(i.thumb),
                                mime_type=self.guess_mime_type(
                                    i.media) or "video/mp4",
                                attributes=[
                                    raw.types.DocumentAttributeVideo(
                                        supports_streaming=i.supports_streaming or None,
                                        duration=i.duration,
                                        w=i.width,
                                        h=i.height
                                    ),
                                    raw.types.DocumentAttributeFilename(
                                        file_name=os.path.basename(i.media))
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
                elif re.match("^https?://", i.media):
                    media = await self.send(
                        raw.functions.messages.UploadMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=raw.types.InputMediaDocumentExternal(
                                url=i.media
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
                else:
                    media = utils.get_input_media_from_file_id(
                        i.media, i.file_ref, 4)

            multi_media.append(
                raw.types.InputSingleMedia(
                    media=media,
                    random_id=self.rnd_id(),
                    **await self.parser.parse(i.caption, i.parse_mode)
                )
            )

        r = await self.send(
            raw.functions.messages.SendMultiMedia(
                peer=await self.resolve_peer(chat_id),
                multi_media=multi_media,
                silent=disable_notification or None,
                reply_to_msg_id=reply_to_message_id
            )
        )

        return await utils.parse_messages(
            self,
            raw.types.messages.Messages(
                messages=[m.message for m in filter(
                    lambda u: isinstance(
                        u, (raw.types.UpdateNewMessage, raw.types.UpdateNewChannelMessage)),
                    r.updates
                )],
                users=r.users,
                chats=r.chats
            )
        )
