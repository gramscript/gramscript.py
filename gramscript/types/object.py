import gramscript
from json import dumps
from datetime import datetime
import typing
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


class Meta(type, metaclass=type("", (type,), {"__str__": lambda _: "~hi"})):
    def __str__(self):
        return f"<class 'gramscript.types.{self.__name__}'>"


class Object(metaclass=Meta):
    def __init__(self, client: "gramscript.Client" = None):
        self._client = client

    def bind(self, client: "gramscript.Client"):
        """Bind a Client instance to this gramscript Object

        Parameters:
            client (:obj:`~gramscript.types.Client`):
                The Client instance to bind this object with. Useful to re-enable bound methods after serializing and
                deserializing gramscript objects with ``repr`` and ``eval``.
        """
        self._client = client

    @staticmethod
    def default(obj: "Object"):
        if isinstance(obj, bytes):
            return repr(obj)

        # https://t.me/gramscriptchat/167281
        # Instead of re.Match, which breaks for python <=3.6
        if isinstance(obj, typing.Match):
            return repr(obj)

        return {
            "_": obj.__class__.__name__,
            **{
                attr: (
                    "*" * len(getattr(obj, attr))
                    if attr == "phone_number" else
                    str(datetime.fromtimestamp(getattr(obj, attr)))
                    if attr.endswith("date") else
                    getattr(obj, attr)
                )
                for attr in filter(lambda x: not x.startswith("_"), obj.__dict__)
                if getattr(obj, attr) is not None
            }
        }

    def __str__(self) -> str:
        return dumps(self, indent=4, default=Object.default, ensure_ascii=False)

    def __repr__(self) -> str:
        return "gramscript.types.{}({})".format(
            self.__class__.__name__,
            ", ".join(
                f"{attr}={repr(getattr(self, attr))}"
                for attr in filter(lambda x: not x.startswith("_"), self.__dict__)
                if getattr(self, attr) is not None
            )
        )

    def __eq__(self, other: "Object") -> bool:
        for attr in self.__dict__:
            try:
                if getattr(self, attr) != getattr(other, attr):
                    return False
            except AttributeError:
                return False

        return True

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)
