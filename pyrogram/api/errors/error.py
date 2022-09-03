

import re
from importlib import import_module

from gramscript.api.types import RpcError
from .exceptions.all import exceptions


class Error(Exception):
    """This is the base exception class for all Telegram API related errors.
    For a finer grained control, see the specific errors below.
    """
    ID = None
    CODE = None
    NAME = None
    MESSAGE = None

    def __init__(self, x: int or RpcError = None, query_type: type = None):
        super().__init__("[{} {}]: {}".format(
            self.CODE, self.ID or self.NAME, self.MESSAGE.format(x=x)))

        try:
            self.x = int(x)
        except (ValueError, TypeError):
            self.x = x

        # TODO: Proper log unknown errors
        if self.CODE == 520:
            with open("unknown_errors.txt", "a") as f:
                f.write("{}\t{}\t{}\n".format(
                    x.error_code, x.error_message, query_type))

    @staticmethod
    def raise_it(rpc_error: RpcError, query_type: type):
        code = rpc_error.error_code

        if code not in exceptions:
            raise UnknownError(rpc_error, query_type)

        message = rpc_error.error_message
        id = re.sub(r"_\d+", "_X", message)

        if id not in exceptions[code]:
            raise UnknownError(rpc_error, query_type)

        x = re.search(r"_(\d+)", message)
        x = x.group(1) if x is not None else x

        raise getattr(
            import_module("gramscript.api.errors"),
            exceptions[code][id]
        )(x)


class UnknownError(Error):
    """This object represents an Unknown Error, that is, an error which
    gramscript does not know anything about, yet.
    """
    CODE = 520
    """:obj:`int`: Error code"""
    NAME = "Unknown error"
    MESSAGE = "{x}"
