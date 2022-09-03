

import logging
import platform
import threading
from datetime import timedelta, datetime
from hashlib import sha1, sha256
from io import BytesIO
from os import urandom
from queue import Queue
from threading import Event, Thread

from gramscript import __copyright__, __license__, __version__
from gramscript.api import functions, types, core
from gramscript.api.all import layer
from gramscript.api.core import Message, Object, MsgContainer, Long, FutureSalt, Int
from gramscript.api.errors import Error
from gramscript.connection import Connection
from gramscript.crypto import IGE, KDF
from .internals import MsgId, MsgFactory, DataCenter

log = logging.getLogger(__name__)


class Result:
    def __init__(self):
        self.value = None
        self.event = Event()


class Session:
    VERSION = __version__
    APP_VERSION = "gramscript \U0001f525 {}".format(VERSION)

    DEVICE_MODEL = "{} {}".format(
        platform.python_implementation(),
        platform.python_version()
    )

    SYSTEM_VERSION = "{} {}".format(
        platform.system(),
        platform.release()
    )

    INITIAL_SALT = 0x616e67656c696361

    WORKERS = 4
    WAIT_TIMEOUT = 10
    MAX_RETRIES = 5
    ACKS_THRESHOLD = 8
    PING_INTERVAL = 5

    notice_displayed = False

    def __init__(self, dc_id: int, test_mode: bool, proxy: type, auth_key: bytes, api_id: str, is_cdn: bool = False):
        if not Session.notice_displayed:
            print("gramscript v{}, {}".format(__version__, __copyright__))
            print("Licensed under the terms of the " + __license__, end="\n\n")
            Session.notice_displayed = True

        self.is_cdn = is_cdn

        self.connection = Connection(DataCenter(dc_id, test_mode), proxy)

        self.api_id = api_id

        self.auth_key = auth_key
        self.auth_key_id = sha1(auth_key).digest()[-8:]

        self.msg_id = MsgId()
        self.session_id = Long(self.msg_id())
        self.msg_factory = MsgFactory(self.msg_id)

        self.current_salt = None

        self.pending_acks = set()

        self.recv_queue = Queue()
        self.results = {}

        self.ping_thread = None
        self.ping_thread_event = Event()

        self.next_salt_thread = None
        self.next_salt_thread_event = Event()

        self.is_connected = Event()

        self.update_handler = None

        self.total_connections = 0
        self.total_messages = 0
        self.total_bytes = 0

    def start(self):
        terms = None

        while True:
            try:
                self.connection.connect()

                for i in range(self.WORKERS):
                    Thread(target=self.worker,
                           name="Worker#{}".format(i + 1)).start()

                Thread(target=self.recv, name="RecvThread").start()

                self.current_salt = FutureSalt(0, 0, self.INITIAL_SALT)
                self.current_salt = FutureSalt(
                    0, 0, self._send(functions.Ping(0)).new_server_salt)
                self.current_salt = self._send(
                    functions.GetFutureSalts(1)).salts[0]

                self.next_salt_thread = Thread(
                    target=self.next_salt, name="NextSaltThread")
                self.next_salt_thread.start()

                if not self.is_cdn:
                    terms = self._send(
                        functions.InvokeWithLayer(
                            layer,
                            functions.InitConnection(
                                self.api_id,
                                self.DEVICE_MODEL,
                                self.SYSTEM_VERSION,
                                self.APP_VERSION,
                                "en", "", "en",
                                functions.help.GetTermsOfService(),
                            )
                        )
                    ).text

                self.ping_thread = Thread(target=self.ping, name="PingThread")
                self.ping_thread.start()

                log.info("Connection inited: Layer {}".format(layer))
            except (OSError, TimeoutError):
                self.stop()
            else:
                break

        self.is_connected.set()
        self.total_connections += 1

        log.debug("Session started")

        return terms

    def stop(self):
        self.is_connected.clear()

        self.ping_thread_event.set()
        self.next_salt_thread_event.set()

        if self.ping_thread is not None:
            self.ping_thread.join()

        if self.next_salt_thread is not None:
            self.next_salt_thread.join()

        self.ping_thread_event.clear()
        self.next_salt_thread_event.clear()

        self.connection.close()

        for i in range(self.WORKERS):
            self.recv_queue.put(None)

        log.debug("Session stopped")

    def restart(self):
        self.stop()
        self.start()

    def pack(self, message: Message):
        data = Long(self.current_salt.salt) + self.session_id + message.write()
        # MTProto 2.0 requires a minimum of 12 padding bytes.
        # I don't get why it says up to 1024 when what it actually needs after the
        # required 12 bytes is just extra 0..15 padding bytes for aes
        # TODO: It works, but recheck this. What's the meaning of 12..1024 padding bytes?
        padding = urandom(-(len(data) + 12) % 16 + 12)

        # 88 = 88 + 0 (outgoing message)
        msg_key_large = sha256(
            self.auth_key[88: 88 + 32] + data + padding).digest()
        msg_key = msg_key_large[8:24]
        aes_key, aes_iv = KDF(self.auth_key, msg_key, True)

        return self.auth_key_id + msg_key + IGE.encrypt(data + padding, aes_key, aes_iv)

    def unpack(self, b: BytesIO) -> Message:
        assert b.read(8) == self.auth_key_id, b.getvalue()

        msg_key = b.read(16)
        aes_key, aes_iv = KDF(self.auth_key, msg_key, False)
        data = BytesIO(IGE.decrypt(b.read(), aes_key, aes_iv))
        data.read(8)

        # https://core.telegram.org/mtproto/security_guidelines#checking-session-id
        assert data.read(8) == self.session_id

        message = Message.read(data)

        # https://core.telegram.org/mtproto/security_guidelines#checking-sha256-hash-value-of-msg-key
        # https://core.telegram.org/mtproto/security_guidelines#checking-message-length
        # 96 = 88 + 8 (incoming message)
        assert msg_key == sha256(
            self.auth_key[96:96 + 32] + data.getvalue()).digest()[8:24]

        # https://core.telegram.org/mtproto/security_guidelines#checking-msg-id
        # TODO: check for lower msg_ids
        assert message.msg_id % 2 != 0

        return message

    def worker(self):
        name = threading.current_thread().name
        log.debug("{} started".format(name))

        while True:
            packet = self.recv_queue.get()

            if packet is None:
                break

            try:
                self.unpack_dispatch_and_ack(packet)
            except Exception as e:
                log.error(e, exc_info=True)

        log.debug("{} stopped".format(name))

    def unpack_dispatch_and_ack(self, packet: bytes):
        # TODO: A better dispatcher
        data = self.unpack(BytesIO(packet))

        messages = (
            data.body.messages
            if isinstance(data.body, MsgContainer)
            else [data]
        )

        log.debug(data)

        self.total_bytes += len(packet)
        self.total_messages += len(messages)

        for i in messages:
            if i.seq_no % 2 != 0:
                if i.msg_id in self.pending_acks:
                    continue
                else:
                    self.pending_acks.add(i.msg_id)

            # log.debug("{}".format(type(i.body)))

            if isinstance(i.body, (types.MsgDetailedInfo, types.MsgNewDetailedInfo)):
                self.pending_acks.add(i.body.answer_msg_id)
                continue

            if isinstance(i.body, types.NewSessionCreated):
                continue

            msg_id = None

            if isinstance(i.body, (types.BadMsgNotification, types.BadServerSalt)):
                msg_id = i.body.bad_msg_id
            elif isinstance(i.body, (core.FutureSalts, types.RpcResult)):
                msg_id = i.body.req_msg_id
            elif isinstance(i.body, types.Pong):
                msg_id = i.body.msg_id
            else:
                if self.update_handler:
                    self.update_handler(i.body)

            if msg_id in self.results:
                self.results[msg_id].value = getattr(i.body, "result", i.body)
                self.results[msg_id].event.set()

        # print(
        #     "This packet bytes: ({}) | Total bytes: ({})\n"
        #     "This packet messages: ({}) | Total messages: ({})\n"
        #     "Total connections: ({})".format(
        #         len(packet), self.total_bytes, len(messages), self.total_messages, self.total_connections
        #     )
        # )

        if len(self.pending_acks) >= self.ACKS_THRESHOLD:
            log.info("Send {} acks".format(len(self.pending_acks)))

            try:
                self._send(types.MsgsAck(list(self.pending_acks)), False)
            except (OSError, TimeoutError):
                pass
            else:
                self.pending_acks.clear()

    def ping(self):
        log.debug("PingThread started")

        while True:
            self.ping_thread_event.wait(self.PING_INTERVAL)

            if self.ping_thread_event.is_set():
                break

            try:
                self._send(functions.Ping(0), False)
            except (OSError, TimeoutError):
                pass

        log.debug("PingThread stopped")

    def next_salt(self):
        log.debug("NextSaltThread started")

        while True:
            now = datetime.now()

            # Seconds to wait until middle-overlap, which is
            # 15 minutes before/after the current/next salt end/start time
            dt = (self.current_salt.valid_until - now).total_seconds() - 900

            log.debug("Current salt: {} | Next salt in {:.0f}m {:.0f}s ({})".format(
                self.current_salt.salt,
                dt // 60,
                dt % 60,
                now + timedelta(seconds=dt)
            ))

            self.next_salt_thread_event.wait(dt)

            if self.next_salt_thread_event.is_set():
                break

            try:
                self.current_salt = self._send(
                    functions.GetFutureSalts(1)).salts[0]
            except (OSError, TimeoutError):
                self.connection.close()
                break

        log.debug("NextSaltThread stopped")

    def recv(self):
        log.debug("RecvThread started")

        while True:
            packet = self.connection.recv()

            if packet is None or (len(packet) == 4 and Int.read(BytesIO(packet)) == -404):
                if self.is_connected.is_set():
                    Thread(target=self.restart, name="RestartThread").start()
                break

            self.recv_queue.put(packet)

        log.debug("RecvThread stopped")

    def _send(self, data: Object, wait_response: bool = True):
        message = self.msg_factory(data)
        msg_id = message.msg_id

        if wait_response:
            self.results[msg_id] = Result()

        payload = self.pack(message)

        try:
            self.connection.send(payload)
        except OSError as e:
            self.results.pop(msg_id, None)
            raise e

        if wait_response:
            self.results[msg_id].event.wait(self.WAIT_TIMEOUT)
            result = self.results.pop(msg_id).value

            if result is None:
                raise TimeoutError
            elif isinstance(result, types.RpcError):
                Error.raise_it(result, type(data))
            else:
                return result

    def send(self, data: Object):
        for i in range(self.MAX_RETRIES):
            self.is_connected.wait()

            try:
                return self._send(data)
            except (OSError, TimeoutError):
                log.warning("Retrying {}".format(type(data)))
                continue
        else:
            return None
