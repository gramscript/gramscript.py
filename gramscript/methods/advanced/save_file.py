from gramscript.session import Session
from gramscript.scaffold import Scaffold
from gramscript import raw
from gramscript import StopTransmission
from typing import Union, BinaryIO
from pathlib import PurePath
from hashlib import md5
import os
import math
import logging
import io
import inspect
import functools
import asyncio
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


log = logging.getLogger(__name__)


class SaveFile(Scaffold):
    async def save_file(
        self,
        path: Union[str, BinaryIO],
        file_id: int = None,
        file_part: int = 0,
        progress: callable = None,
        progress_args: tuple = ()
    ):
        """Upload a file onto Telegram servers, without actually sending the message to anyone.
        Useful whenever an InputFile type is required.

        .. note::

            This is a utility method intended to be used **only** when working with raw
            :obj:`functions <gramscript.api.functions>` (i.e: a Telegram API method you wish to use which is not
            available yet in the Client class as an easy-to-use method).

        Parameters:
            path (``str``):
                The path of the file you want to upload that exists on your local machine.

            file_id (``int``, *optional*):
                In case a file part expired, pass the file_id and the file_part to retry uploading that specific chunk.

            file_part (``int``, *optional*):
                In case a file part expired, pass the file_id and the file_part to retry uploading that specific chunk.

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
            ``InputFile``: On success, the uploaded file is returned in form of an InputFile object.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if path is None:
            return None

        async def worker(session):
            while True:
                data = await queue.get()

                if data is None:
                    return

                try:
                    await self.loop.create_task(session.send(data))
                except Exception as e:
                    log.error(e)

        part_size = 512 * 1024

        if isinstance(path, (str, PurePath)):
            fp = open(path, "rb")
        elif isinstance(path, io.IOBase):
            fp = path
        else:
            raise ValueError(
                "Invalid file. Expected a file path as string or a binary (not text) file pointer")

        file_name = fp.name

        fp.seek(0, os.SEEK_END)
        file_size = fp.tell()
        fp.seek(0)

        if file_size == 0:
            raise ValueError("File size equals to 0 B")

        if file_size > 2000 * 1024 * 1024:
            raise ValueError(
                "Telegram doesn't support uploading files bigger than 2000 MiB")

        file_total_parts = int(math.ceil(file_size / part_size))
        is_big = file_size > 10 * 1024 * 1024
        pool_size = 3 if is_big else 1
        workers_count = 4 if is_big else 1
        is_missing_part = file_id is not None
        file_id = file_id or self.rnd_id()
        md5_sum = md5() if not is_big and not is_missing_part else None
        pool = [
            Session(
                self, await self.storage.dc_id(), await self.storage.auth_key(),
                await self.storage.test_mode(), is_media=True
            ) for _ in range(pool_size)
        ]
        workers = [self.loop.create_task(worker(session))
                   for session in pool for _ in range(workers_count)]
        queue = asyncio.Queue(16)

        try:
            for session in pool:
                await session.start()

            with fp:
                fp.seek(part_size * file_part)

                while True:
                    chunk = fp.read(part_size)

                    if not chunk:
                        if not is_big:
                            md5_sum = "".join([hex(i)[2:].zfill(2)
                                              for i in md5_sum.digest()])
                        break

                    if is_big:
                        rpc = raw.functions.upload.SaveBigFilePart(
                            file_id=file_id,
                            file_part=file_part,
                            file_total_parts=file_total_parts,
                            bytes=chunk
                        )
                    else:
                        rpc = raw.functions.upload.SaveFilePart(
                            file_id=file_id,
                            file_part=file_part,
                            bytes=chunk
                        )

                    await queue.put(rpc)

                    if is_missing_part:
                        return

                    if not is_big:
                        md5_sum.update(chunk)

                    file_part += 1

                    if progress:
                        if inspect.iscoroutinefunction(progress):
                            await progress(min(file_part * part_size, file_size), file_size, *progress_args)
                        else:
                            func = functools.partial(
                                progress,
                                min(file_part * part_size, file_size),
                                file_size,
                                *progress_args
                            )

                            await self.loop.run_in_executor(self.executor, func)
        except StopTransmission:
            raise
        except Exception as e:
            log.error(e, exc_info=True)
        else:
            if is_big:
                return raw.types.InputFileBig(
                    id=file_id,
                    parts=file_total_parts,
                    name=file_name,

                )
            else:
                return raw.types.InputFile(
                    id=file_id,
                    parts=file_total_parts,
                    name=file_name,
                    md5_checksum=md5_sum
                )
        finally:
            for _ in workers:
                await queue.put(None)

            await asyncio.gather(*workers)

            for session in pool:
                await session.stop()
