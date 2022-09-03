

from collections import OrderedDict
from datetime import datetime
from io import BytesIO
from json import JSONEncoder, dumps

from ..all import objects


class Object:
    all = {}

    @staticmethod
    def read(b: BytesIO, *args):
        return Object.all[int.from_bytes(b.read(4), "little")].read(b, *args)

    def write(self, *args) -> bytes:
        pass

    def __str__(self) -> str:
        return dumps(self, cls=Encoder, indent=4)

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__

    def __len__(self) -> int:
        return len(self.write())

    def __call__(self):
        pass


class Encoder(JSONEncoder):
    def default(self, o: Object):
        try:
            content = o.__dict__
        except AttributeError:
            if isinstance(o, datetime):
                return o.strftime("%d-%b-%Y %H:%M:%S")
            else:
                return repr(o)

        return OrderedDict(
            [("_", objects.get(getattr(o, "ID", None), None))]
            + [i for i in content.items()]
        )
