from ..all import objects
from typing import cast, List, Any, Union, Dict
from json import dumps
from io import BytesIO
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


class TLObject:
    __slots__: List[str] = []

    QUALNAME = "Base"

    @classmethod
    def read(cls, data: BytesIO, *args: Any) -> Any:
        return cast(TLObject, objects[int.from_bytes(data.read(4), "little")]).read(data, *args)

    def write(self, *args: Any) -> bytes:
        pass

    @staticmethod
    def default(obj: "TLObject") -> Union[str, Dict[str, str]]:
        if isinstance(obj, bytes):
            return repr(obj)

        return {
            "_": obj.QUALNAME,
            **{
                attr: getattr(obj, attr)
                for attr in obj.__slots__
                if getattr(obj, attr) is not None
            }
        }

    def __str__(self) -> str:
        return dumps(self, indent=4, default=TLObject.default, ensure_ascii=False)

    def __repr__(self) -> str:
        return "gramscript.api.{}({})".format(
            self.QUALNAME,
            ", ".join(
                f"{attr}={repr(getattr(self, attr))}"
                for attr in self.__slots__
                if getattr(self, attr) is not None
            )
        )

    def __eq__(self, other: Any) -> bool:
        for attr in self.__slots__:
            try:
                if getattr(self, attr) != getattr(other, attr):
                    return False
            except AttributeError:
                return False

        return True

    def __len__(self) -> int:
        return len(self.write())

    def __getitem__(self, item: Any) -> Any:
        return getattr(self, item)

    def __setitem__(self, key: Any, value: Any) -> Any:
        setattr(self, key, value)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        pass
