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

from hashlib import sha256
from io import BytesIO
from os import urandom

from gramscript.raw.core import Message, Long
from . import aes


def kdf(auth_key: bytes, msg_key: bytes, outgoing: bool) -> tuple:
    # https://core.telegram.org/mtproto/description#defining-aes-key-and-initialization-vector
    x = 0 if outgoing else 8

    sha256_a = sha256(msg_key + auth_key[x: x + 36]).digest()
    sha256_b = sha256(auth_key[x + 40:x + 76] +
                      msg_key).digest()  # 76 = 40 + 36

    aes_key = sha256_a[:8] + sha256_b[8:24] + sha256_a[24:32]
    aes_iv = sha256_b[:8] + sha256_a[8:24] + sha256_b[24:32]

    return aes_key, aes_iv


def pack(message: Message, salt: int, session_id: bytes, auth_key: bytes, auth_key_id: bytes) -> bytes:
    data = Long(salt) + session_id + message.write()
    padding = urandom(-(len(data) + 12) % 16 + 12)

    # 88 = 88 + 0 (outgoing message)
    msg_key_large = sha256(auth_key[88: 88 + 32] + data + padding).digest()
    msg_key = msg_key_large[8:24]
    aes_key, aes_iv = kdf(auth_key, msg_key, True)

    return auth_key_id + msg_key + aes.ige256_encrypt(data + padding, aes_key, aes_iv)


def unpack(b: BytesIO, session_id: bytes, auth_key: bytes, auth_key_id: bytes) -> Message:
    assert b.read(8) == auth_key_id, b.getvalue()

    msg_key = b.read(16)
    aes_key, aes_iv = kdf(auth_key, msg_key, False)
    data = BytesIO(aes.ige256_decrypt(b.read(), aes_key, aes_iv))
    data.read(8)

    # https://core.telegram.org/mtproto/security_guidelines#checking-session-id
    assert data.read(8) == session_id

    message = Message.read(data)

    # https://core.telegram.org/mtproto/security_guidelines#checking-sha256-hash-value-of-msg-key
    # https://core.telegram.org/mtproto/security_guidelines#checking-message-length
    # 96 = 88 + 8 (incoming message)
    assert msg_key == sha256(
        auth_key[96:96 + 32] + data.getvalue()).digest()[8:24]

    # https://core.telegram.org/mtproto/security_guidelines#checking-msg-id
    assert message.msg_id % 2 != 0

    return message
