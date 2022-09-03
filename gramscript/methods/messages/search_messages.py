from gramscript.scaffold import Scaffold
from gramscript import utils
from gramscript import types
from gramscript import raw
from typing import Union, List, AsyncGenerator, Optional
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


class Filters:
    EMPTY = raw.types.InputMessagesFilterEmpty()
    PHOTO = raw.types.InputMessagesFilterPhotos()
    VIDEO = raw.types.InputMessagesFilterVideo()
    PHOTO_VIDEO = raw.types.InputMessagesFilterPhotoVideo()
    DOCUMENT = raw.types.InputMessagesFilterDocument()
    URL = raw.types.InputMessagesFilterUrl()
    ANIMATION = raw.types.InputMessagesFilterGif()
    VOICE_NOTE = raw.types.InputMessagesFilterVoice()
    AUDIO = raw.types.InputMessagesFilterMusic()
    CHAT_PHOTO = raw.types.InputMessagesFilterChatPhotos()
    PHONE_CALL = raw.types.InputMessagesFilterPhoneCalls()
    AUDIO_VIDEO_NOTE = raw.types.InputMessagesFilterRoundVideo()
    VIDEO_NOTE = raw.types.InputMessagesFilterRoundVideo()
    MENTION = raw.types.InputMessagesFilterMyMentions()
    LOCATION = raw.types.InputMessagesFilterGeo()
    CONTACT = raw.types.InputMessagesFilterContacts()


POSSIBLE_VALUES = list(map(lambda x: x.lower(), filter(
    lambda x: not x.startswith("__"), Filters.__dict__.keys())))


# noinspection PyShadowingBuiltins
async def get_chunk(
    client: Scaffold,
    chat_id: Union[int, str],
    query: str = "",
    filter: str = "empty",
    offset: int = 0,
    limit: int = 100,
    from_user: Union[int, str] = None
) -> List["types.Message"]:
    try:
        filter = Filters.__dict__[filter.upper()]
    except KeyError:
        raise ValueError('Invalid filter "{}". Possible values are: {}'.format(
            filter, ", ".join(f'"{v}"' for v in POSSIBLE_VALUES))) from None

    r = await client.send(
        raw.functions.messages.Search(
            peer=await client.resolve_peer(chat_id),
            q=query,
            filter=filter,
            min_date=0,
            max_date=0,
            offset_id=0,
            add_offset=offset,
            limit=limit,
            min_id=0,
            max_id=0,
            from_id=(
                await client.resolve_peer(from_user)
                if from_user
                else None
            ),
            hash=0
        )
    )

    return await utils.parse_messages(client, r)


class SearchMessages(Scaffold):
    # noinspection PyShadowingBuiltins
    async def search_messages(
        self,
        chat_id: Union[int, str],
        query: str = "",
        offset: int = 0,
        filter: str = "empty",
        limit: int = 0,
        from_user: Union[int, str] = None
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        """Search for text and media messages inside a specific chat.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            query (``str``, *optional*):
                Text query string.
                Required for text-only messages, optional for media messages (see the ``filter`` argument).
                When passed while searching for media messages, the query will be applied to captions.
                Defaults to "" (empty string).

            offset (``int``, *optional*):
                Sequential number of the first message to be returned.
                Defaults to 0.

            filter (``str``, *optional*):
                Pass a filter in order to search for specific kind of messages only:

                - ``"empty"``: Search for all kind of messages (default).
                - ``"photo"``: Search for photos.
                - ``"video"``: Search for video.
                - ``"photo_video"``: Search for either photo or video.
                - ``"document"``: Search for documents (generic files).
                - ``"url"``: Search for messages containing URLs (web links).
                - ``"animation"``: Search for animations (GIFs).
                - ``"voice_note"``: Search for voice notes.
                - ``"audio"``: Search for audio files (music).
                - ``"chat_photo"``: Search for chat photos.
                - ``"phone_call"``: Search for phone calls.
                - ``"audio_video_note"``: Search for either audio or video notes.
                - ``"video_note"``: Search for video notes.
                - ``"mention"``: Search for messages containing mentions to yourself.
                - ``"location"``: Search for location messages.
                - ``"contact"``: Search for contact messages.

            limit (``int``, *optional*):
                Limits the number of messages to be retrieved.
                By default, no limit is applied and all messages are returned.

            from_user (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user you want to search for messages from.

        Returns:
            ``Generator``: A generator yielding :obj:`~gramscript.types.Message` objects.

        Example:
            .. code-block:: python

                # Search for text messages in @gramscriptchat. Get the last 333 results
                for message in app.search_messages("gramscriptchat", query="dan", limit=333):
                    print(message.text)

                # Search for photos sent by @haskell in @gramscriptchat
                for message in app.search_messages("gramscriptchat", "", filter="photo" limit=333, from_user="haskell"):
                    print(message.text)
        """
        current = 0
        total = abs(limit) or (1 << 31) - 1
        limit = min(100, total)

        while True:
            messages = await get_chunk(
                client=self,
                chat_id=chat_id,
                query=query,
                filter=filter,
                offset=offset,
                limit=limit,
                from_user=from_user
            )

            if not messages:
                return

            offset += 100

            for message in messages:
                yield message

                current += 1

                if current >= total:
                    return
