

from io import BytesIO

from . import Bytes


class String(Bytes):
    @staticmethod
    def read(b: BytesIO, *args) -> str:
        return super(String, String).read(b).decode()

    def __new__(cls, value: str) -> bytes:
        return super().__new__(cls, value.encode())
