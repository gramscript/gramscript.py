from gramscript.scaffold import Scaffold
from gramscript import types
from gramscript import raw
from typing import Union
from typing import List
from getpass import getpass
from concurrent.futures.thread import ThreadPoolExecutor
import struct
import os
import hashlib
import functools
import base64
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


def decode_file_id(s: str) -> bytes:
    s = base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))
    r = b""

    major = s[-1]
    minor = s[-2] if major != 2 else 0

    assert minor in (0, 22, 24)

    skip = 2 if minor else 1

    i = 0

    while i < len(s) - skip:
        if s[i] != 0:
            r += bytes([s[i]])
        else:
            r += b"\x00" * s[i + 1]
            i += 1

        i += 1

    return r


def encode_file_id(s: bytes) -> str:
    r = b""
    n = 0

    for i in s + bytes([22]) + bytes([4]):
        if i == 0:
            n += 1
        else:
            if n:
                r += b"\x00" + bytes([n])
                n = 0

            r += bytes([i])

    return base64.urlsafe_b64encode(r).decode().rstrip("=")


def encode_file_ref(file_ref: bytes) -> str:
    return base64.urlsafe_b64encode(file_ref).decode().rstrip("=")


def decode_file_ref(file_ref: str) -> bytes:
    if file_ref is None:
        return b""

    return base64.urlsafe_b64decode(file_ref + "=" * (-len(file_ref) % 4))


async def ainput(prompt: str = "", *, hide: bool = False):
    with ThreadPoolExecutor(1) as executor:
        func = functools.partial(getpass if hide else input, prompt)
        return await asyncio.get_event_loop().run_in_executor(executor, func)


def get_offset_date(dialogs):
    return next((m.date for m in reversed(dialogs.messages) if not isinstance(m, raw.types.MessageEmpty)), 0)


def get_input_media_from_file_id(file_id_str: str, file_ref: str = None, expected_media_type: int = None) -> Union["raw.types.InputMediaPhoto", "raw.types.InputMediaDocument"]:
    try:
        decoded = decode_file_id(file_id_str)
    except Exception:
        raise ValueError(f"Failed to decode file_id: {file_id_str}")
    else:
        media_type = decoded[0]
        if expected_media_type is not None and media_type != expected_media_type:
            media_type_str = Scaffold.MEDIA_TYPE_ID.get(media_type, None)
            expected_media_type_str = Scaffold.MEDIA_TYPE_ID.get(
                expected_media_type, None)
            raise ValueError(
                f'Expected: "{expected_media_type_str}", got "{media_type_str}" file_id instead')

        if media_type in (0, 1, 14):
            raise ValueError(
                f"This file_id can only be used for download: {file_id_str}")
        if media_type == 2:
            unpacked = struct.unpack("<iiqqqiiii", decoded)
            dc_id, file_id, access_hash, volume_id, _, _, type, local_id = unpacked[1:]
            return raw.types.InputMediaPhoto(id=raw.types.InputPhoto(id=file_id, access_hash=access_hash, file_reference=decode_file_ref(file_ref)))

        if media_type in (3, 4, 5, 8, 9, 10, 13):
            unpacked = struct.unpack("<iiqq", decoded)
            dc_id, file_id, access_hash = unpacked[1:]
            return raw.types.InputMediaDocument(id=raw.types.InputDocument(id=file_id, access_hash=access_hash, file_reference=decode_file_ref(file_ref)))

        raise ValueError(f"Unknown media type: {file_id_str}")


async def parse_messages(client, messages: "raw.types.messages.Messages", replies: int = 1) -> List["types.Message"]:
    users = {i.id: i for i in messages.users}
    chats = {i.id: i for i in messages.chats}

    if not messages.messages:
        return types.List()

    parsed_messages = []

    for message in messages.messages:
        parsed_messages.append(await types.Message._parse(client, message, users, chats, replies=0))

    if replies:
        messages_with_replies = {i.id: getattr(
            i, "reply_to_msg_id", None) for i in messages.messages}
        reply_message_ids = [i[0] for i in filter(
            lambda x: x[1] is not None, messages_with_replies.items())]

        if reply_message_ids:
            reply_messages = await client.get_messages(
                parsed_messages[0].chat.id,
                reply_to_message_ids=reply_message_ids,
                replies=replies - 1
            )

            for message in parsed_messages:
                reply_id = messages_with_replies[message.message_id]

                for reply in reply_messages:
                    if reply.message_id == reply_id:
                        message.reply_to_message = reply

    return types.List(parsed_messages)


def parse_deleted_messages(client, update) -> List["types.Message"]:
    messages = update.messages
    channel_id = getattr(update, "channel_id", None)
    parsed_messages = [types.Message(message_id=message, chat=types.Chat(id=get_channel_id(
        channel_id), type="channel", client=client) if channel_id is not None else None, client=client) for message in messages]

    return types.List(parsed_messages)


def unpack_inline_message_id(inline_message_id: str) -> "raw.types.InputBotInlineMessageID":
    r = inline_message_id + "=" * (-len(inline_message_id) % 4)
    r = struct.unpack("<iqq", base64.b64decode(r, altchars=b"-_"))

    return raw.types.InputBotInlineMessageID(
        dc_id=r[0],
        id=r[1],
        access_hash=r[2]
    )


MIN_CHANNEL_ID = -1002147483647
MAX_CHANNEL_ID = -1000000000000
MIN_CHAT_ID = -2147483647
MAX_USER_ID = 2147483647


def get_peer_id(peer: raw.base.Peer) -> int:
    if isinstance(peer, raw.types.PeerUser):
        return peer.user_id

    if isinstance(peer, raw.types.PeerChat):
        return -peer.chat_id

    if isinstance(peer, raw.types.PeerChannel):
        return MAX_CHANNEL_ID - peer.channel_id

    raise ValueError(f"Peer type invalid: {peer}")


def get_peer_type(peer_id: int) -> str:
    if peer_id < 0:
        if MIN_CHAT_ID <= peer_id:
            return "chat"

        if MIN_CHANNEL_ID <= peer_id < MAX_CHANNEL_ID:
            return "channel"
    elif 0 < peer_id <= MAX_USER_ID:
        return "user"

    raise ValueError(f"Peer id invalid: {peer_id}")


def get_channel_id(peer_id: int) -> int:
    return MAX_CHANNEL_ID - peer_id


def btoi(b: bytes) -> int:
    return int.from_bytes(b, "big")


def itob(i: int) -> bytes:
    return i.to_bytes(256, "big")


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(i ^ j for i, j in zip(a, b))


def compute_password_hash(algo: raw.types.PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow,
                          password: str) -> bytes:
    hash1 = sha256(algo.salt1 + password.encode() + algo.salt1)
    hash2 = sha256(algo.salt2 + hash1 + algo.salt2)
    hash3 = hashlib.pbkdf2_hmac("sha512", hash2, algo.salt1, 100000)

    return sha256(algo.salt2 + hash3 + algo.salt2)


# noinspection PyPep8Naming
def compute_password_check(r: raw.types.account.Password, password: str) -> raw.types.InputCheckPasswordSRP:
    algo = r.current_algo

    p_bytes = algo.p
    p = btoi(algo.p)

    g_bytes = itob(algo.g)
    g = algo.g

    B_bytes = r.srp_B
    B = btoi(B_bytes)

    srp_id = r.srp_id

    x_bytes = compute_password_hash(algo, password)
    x = btoi(x_bytes)

    g_x = pow(g, x, p)

    k_bytes = sha256(p_bytes + g_bytes)
    k = btoi(k_bytes)

    kg_x = (k * g_x) % p

    while True:
        a_bytes = os.urandom(256)
        a = btoi(a_bytes)

        A = pow(g, a, p)
        A_bytes = itob(A)

        u = btoi(sha256(A_bytes + B_bytes))

        if u > 0:
            break

    g_b = (B - kg_x) % p

    ux = u * x
    a_ux = a + ux
    S = pow(g_b, a_ux, p)
    S_bytes = itob(S)

    K_bytes = sha256(S_bytes)

    M1_bytes = sha256(
        xor(sha256(p_bytes), sha256(g_bytes))
        + sha256(algo.salt1)
        + sha256(algo.salt2)
        + A_bytes
        + B_bytes
        + K_bytes
    )

    return raw.types.InputCheckPasswordSRP(srp_id=srp_id, A=A_bytes, M1=M1_bytes)
