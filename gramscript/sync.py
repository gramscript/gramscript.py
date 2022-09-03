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

import asyncio
import functools
import inspect
import threading

from gramscript import types
from gramscript.methods import Methods
from gramscript.methods.utilities import idle as idle_module


def async_to_sync(obj, name):
    function = getattr(obj, name)
    loop = asyncio.get_event_loop()

    async def consume_generator(coroutine):
        return [i async for i in coroutine]

    @functools.wraps(function)
    def async_to_sync_wrap(*args, **kwargs):
        coroutine = function(*args, **kwargs)
        if loop.is_running():
            if threading.current_thread() is threading.main_thread():
                return coroutine
            if inspect.iscoroutine(coroutine):
                return asyncio.run_coroutine_threadsafe(coroutine, loop).result()
            if inspect.isasyncgen(coroutine):
                return asyncio.run_coroutine_threadsafe(consume_generator(coroutine), loop).result()

        if inspect.iscoroutine(coroutine):
            return loop.run_until_complete(coroutine)
        if inspect.isasyncgen(coroutine):
            return loop.run_until_complete(consume_generator(coroutine))

    setattr(obj, name, async_to_sync_wrap)


def wrap(source):
    for name in dir(source):
        method = getattr(source, name)

        if not name.startswith("_") and (inspect.iscoroutinefunction(method) or inspect.isasyncgenfunction(method)):
            async_to_sync(source, name)


# Wrap all Client's relevant methods
wrap(Methods)

# Wrap types' bound methods
for class_name in dir(types):
    cls = getattr(types, class_name)

    if inspect.isclass(cls):
        wrap(cls)

# Special case for idle, because it's not inside Methods
async_to_sync(idle_module, "idle")
idle = getattr(idle_module, "idle")
