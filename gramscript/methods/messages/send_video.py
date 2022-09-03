from gramscript.scaffold import Scaffold
from gramscript.errors import FilePartMissing
from gramscript import utils
from gramscript import types
from gramscript import raw
from gramscript import StopTransmission
from typing import Union, BinaryIO
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


class SendVideo(Scaffold):
    async def send_video(
        self,
        chat_id: Union[int, str],
        video: Union[str, BinaryIO],
        file_ref: str = None,
        caption: str = "",
        parse_mode: Union[str, None] = object,
        duration: int = 0,
        width: int = 0,
        height: int = 0,
        thumb: Union[str, BinaryIO] = None,
        file_name: str = None,
        supports_streaming: bool = True,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        schedule_date: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: callable = None,
        progress_args: tuple = ()
    ) -> Union["types.Message", None]:
        """Send video files.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            video (``str`` | ``BinaryIO``):
                Video to send.
                Pass a file_id as string to send a video that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a video from the Internet,
                pass a file path as string to upload a new video that exists on your local machine, or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

            file_ref (``str``, *optional*):
                A valid file reference obtained by a recently fetched media message.
                To be used in combination with a file id in case a file reference is needed.

            caption (``str``, *optional*):
                Video caption, 0-1024 characters.

            parse_mode (``str``, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.
                Pass "markdown" or "md" to enable Markdown-style parsing only.
                Pass "html" to enable HTML-style parsing only.
                Pass None to completely disable style parsing.

            duration (``int``, *optional*):
                Duration of sent video in seconds.

            width (``int``, *optional*):
                Video width.

            height (``int``, *optional*):
                Video height.

            thumb (``str`` | ``BinaryIO``, *optional*):
                Thumbnail of the video sent.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 320 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            file_name (``str``, *optional*):
                File name of the video sent.
                Defaults to file's path basename.

            supports_streaming (``bool``, *optional*):
                Pass True, if the uploaded video is suitable for streaming.
                Defaults to True.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            schedule_date (``int``, *optional*):
                Date when the message will be automatically sent. Unix time.

            reply_markup (:obj:`~gramscript.types.InlineKeyboardMarkup` | :obj:`~gramscript.types.ReplyKeyboardMarkup` | :obj:`~gramscript.types.ReplyKeyboardRemove` | :obj:`~gramscript.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the *progress_args* parameter.
                You can either keep *\*args* or add every single extra argument in your function signature.

        Returns:
            :obj:`~gramscript.types.Message` | ``None``: On success, the sent video message is returned, otherwise, in
            case the upload is deliberately stopped with :meth:`~gramscript.Client.stop_transmission`, None is returned.

        Example:
            .. code-block:: python

                # Send video by uploading from local file
                app.send_video("me", "video.mp4")

                # Add caption to the video
                app.send_video("me", "video.mp4", caption="recording")

                # Keep track of the progress while uploading
                def progress(current, total):
                    print(f"{current * 100 / total:.1f}%")

                app.send_video("me", "video.mp4", progress=progress)
        """
        file = None

        try:
            if isinstance(video, str):
                if os.path.isfile(video):
                    thumb = await self.save_file(thumb)
                    file = await self.save_file(video, progress=progress, progress_args=progress_args)
                    media = raw.types.InputMediaUploadedDocument(
                        mime_type=self.guess_mime_type(video) or "video/mp4",
                        file=file,
                        thumb=thumb,
                        attributes=[
                            raw.types.DocumentAttributeVideo(
                                supports_streaming=supports_streaming or None,
                                duration=duration,
                                w=width,
                                h=height
                            ),
                            raw.types.DocumentAttributeFilename(
                                file_name=file_name or os.path.basename(video))
                        ]
                    )
                elif re.match("^https?://", video):
                    media = raw.types.InputMediaDocumentExternal(
                        url=video
                    )
                else:
                    media = utils.get_input_media_from_file_id(
                        video, file_ref, 4)
            else:
                thumb = await self.save_file(thumb)
                file = await self.save_file(video, progress=progress, progress_args=progress_args)
                media = raw.types.InputMediaUploadedDocument(
                    mime_type=self.guess_mime_type(video.name) or "video/mp4",
                    file=file,
                    thumb=thumb,
                    attributes=[
                        raw.types.DocumentAttributeVideo(
                            supports_streaming=supports_streaming or None,
                            duration=duration,
                            w=width,
                            h=height
                        ),
                        raw.types.DocumentAttributeFilename(
                            file_name=video.name)
                    ]
                )

            while True:
                try:
                    r = await self.send(
                        raw.functions.messages.SendMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=media,
                            silent=disable_notification or None,
                            reply_to_msg_id=reply_to_message_id,
                            random_id=self.rnd_id(),
                            schedule_date=schedule_date,
                            reply_markup=reply_markup.write() if reply_markup else None,
                            **await self.parser.parse(caption, parse_mode)
                        )
                    )
                except FilePartMissing as e:
                    await self.save_file(video, file_id=file.id, file_part=e.x)
                else:
                    for i in r.updates:
                        if isinstance(i, (raw.types.UpdateNewMessage,
                                          raw.types.UpdateNewChannelMessage,
                                          raw.types.UpdateNewScheduledMessage)):
                            return await types.Message._parse(
                                self, i.message,
                                {i.id: i for i in r.users},
                                {i.id: i for i in r.chats},
                                is_scheduled=isinstance(
                                    i, raw.types.UpdateNewScheduledMessage)
                            )
        except StopTransmission:
            return None
