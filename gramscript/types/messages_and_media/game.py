from ..object import Object
from gramscript import types
from gramscript import raw
import gramscript
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


class Game(Object):
    """A game.
    Use BotFather to create and edit games, their short names will act as unique identifiers.

    Parameters:
        id (``int``):
            Unique identifier of the game.

        title (``str``):
            Title of the game.

        short_name (``str``):
            Unique short name of the game.

        description (``str``):
            Description of the game.

        photo (:obj:`~gramscript.types.Photo`):
            Photo that will be displayed in the game message in chats.

        animation (:obj:`~gramscript.types.Animation`, *optional*):
            Animation that will be displayed in the game message in chats.
            Upload via BotFather.
    """

    def __init__(
        self,
        *,
        client: "gramscript.Client" = None,
        id: int,
        title: str,
        short_name: str,
        description: str,
        photo: "types.Photo",
        animation: "types.Animation" = None
    ):
        super().__init__(client)

        self.id = id
        self.title = title
        self.short_name = short_name
        self.description = description
        self.photo = photo
        self.animation = animation

    @staticmethod
    def _parse(client, message: "raw.types.Message") -> "Game":
        game: "raw.types.Game" = message.media.game
        animation = None

        if game.document:
            attributes = {type(i): i for i in game.document.attributes}

            file_name = getattr(
                attributes.get(
                    raw.types.DocumentAttributeFilename, None
                ), "file_name", None
            )

            animation = types.Animation._parse(
                client,
                game.document,
                attributes.get(raw.types.DocumentAttributeVideo, None),
                file_name
            )

        return Game(
            id=game.id,
            title=game.title,
            short_name=game.short_name,
            description=game.description,
            photo=types.Photo._parse(client, game.photo),
            animation=animation,
            client=client
        )
