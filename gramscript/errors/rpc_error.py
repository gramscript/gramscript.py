from .exceptions.all import exceptions
from gramscript.raw.core import TLObject
from gramscript import raw
from typing import Type
from importlib import import_module
from datetime import datetime
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


class RPCError(Exception):
    ID = None
    CODE = None
    NAME = None
    MESSAGE = "{x}"

    def __init__(self, x: int or raw.types.RpcError = None, rpc_name: str = None, is_unknown: bool = False):
        super().__init__("[{} {}]: {} {}".format(
            self.CODE,
            self.ID or self.NAME,
            self.MESSAGE.format(x=x),
            f'(caused by "{rpc_name}")' if rpc_name else ""
        ))

        try:
            self.x = int(x)
        except (ValueError, TypeError):
            self.x = x

        if is_unknown:
            with open("unknown_errors.txt", "a", encoding="utf-8") as f:
                f.write(f"{datetime.now()}\t{x}\t{rpc_name}\n")

    @staticmethod
    def raise_it(rpc_error: "raw.types.RpcError", rpc_type: Type[TLObject]):
        error_code = rpc_error.error_code
        error_message = rpc_error.error_message
        rpc_name = ".".join(rpc_type.QUALNAME.split(".")[1:])

        if error_code not in exceptions:
            raise UnknownError(
                x=f"[{error_code} {error_message}]",
                rpc_name=rpc_name,
                is_unknown=True
            )

        error_id = re.sub(r"_\d+", "_X", error_message)

        if error_id not in exceptions[error_code]:
            raise getattr(
                import_module("gramscript.errors"),
                exceptions[error_code]["_"]
            )(x=f"[{error_code} {error_message}]",
              rpc_name=rpc_name,
              is_unknown=True)

        x = re.search(r"_(\d+)", error_message)
        x = x.group(1) if x is not None else x

        raise getattr(
            import_module("gramscript.errors"),
            exceptions[error_code][error_id]
        )(x=x,
          rpc_name=rpc_name,
          is_unknown=False)


class UnknownError(RPCError):
    CODE = 520
    """:obj:`int`: Error code"""
    NAME = "Unknown error"
