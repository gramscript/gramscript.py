from gramscript.session.internals import MsgId
from gramscript.parser import Parser
from gramscript import __version__
from pathlib import Path
import sys
import re
import platform
import os
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


class Scaffold:
    APP_VERSION = f"gramscript {__version__}"
    DEVICE_MODEL = f"{platform.python_implementation()} {platform.python_version()}"
    SYSTEM_VERSION = f"{platform.system()} {platform.release()}"

    LANG_CODE = "en"

    PARENT_DIR = Path(sys.argv[0]).parent

    INVITE_LINK_RE = re.compile(
        r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/joinchat/)([\w-]+)$")
    WORKERS = min(32, os.cpu_count() + 4)
    WORKDIR = PARENT_DIR
    CONFIG_FILE = PARENT_DIR / "config.ini"

    PARSE_MODES = ["combined", "markdown", "md", "html", None]

    MEDIA_TYPE_ID = {
        0: "photo_thumbnail",
        1: "chat_photo",
        2: "photo",
        3: "voice",
        4: "video",
        5: "document",
        8: "sticker",
        9: "audio",
        10: "animation",
        13: "video_note",
        14: "document_thumbnail"
    }

    mime_types_to_extensions = {}
    extensions_to_mime_types = {}

    with open(f"{os.path.dirname(__file__)}/mime.types", "r", encoding="UTF-8") as f:
        for match in re.finditer(r"^([^#\s]+)\s+(.+)$", f.read(), flags=re.M):
            mime_type, extensions = match.groups()

            extensions = [f".{ext}" for ext in extensions.split(" ")]

            for ext in extensions:
                extensions_to_mime_types[ext] = mime_type

            mime_types_to_extensions[mime_type] = " ".join(extensions)

    def __init__(self):
        self.session_name = None
        self.api_id = None
        self.api_hash = None
        self.app_version = None
        self.device_model = None
        self.system_version = None
        self.lang_code = None
        self.ipv6 = None
        self.proxy = None
        self.test_mode = None
        self.bot_token = None
        self.phone_number = None
        self.phone_code = None
        self.password = None
        self.force_sms = None
        self.workers = None
        self.workdir = None
        self.config_file = None
        self.plugins = None
        self.parse_mode = None
        self.no_updates = None
        self.takeout = None
        self.sleep_threshold = None

        self.executor = None

        self.storage = None

        self.rnd_id = MsgId

        self.parser = Parser(self)
        self.parse_mode = "combined"

        self.session = None

        self.media_sessions = {}
        self.media_sessions_lock = asyncio.Lock()

        self.is_connected = None
        self.is_initialized = None

        self.no_updates = None
        self.takeout_id = None

        self.dispatcher = None

        self.disconnect_handler = None

        self.loop = None

    async def send(self, *args, **kwargs):
        pass

    async def resolve_peer(self, *args, **kwargs):
        pass

    def fetch_peers(self, *args, **kwargs):
        pass

    def add_handler(self, *args, **kwargs):
        pass

    async def save_file(self, *args, **kwargs):
        pass

    async def get_messages(self, *args, **kwargs):
        pass

    async def get_history(self, *args, **kwargs):
        pass

    async def get_dialogs(self, *args, **kwargs):
        pass

    async def get_chat_members(self, *args, **kwargs):
        pass

    async def get_chat_members_count(self, *args, **kwargs):
        pass

    async def answer_inline_query(self, *args, **kwargs):
        pass

    async def get_profile_photos(self, *args, **kwargs):
        pass

    async def edit_message_text(self, *args, **kwargs):
        pass

    async def edit_inline_text(self, *args, **kwargs):
        pass

    async def edit_message_media(self, *args, **kwargs):
        pass

    async def edit_inline_media(self, *args, **kwargs):
        pass

    async def edit_message_reply_markup(self, *args, **kwargs):
        pass

    async def edit_inline_reply_markup(self, *args, **kwargs):
        pass

    def guess_mime_type(self, *args, **kwargs):
        pass

    def guess_extension(self, *args, **kwargs):
        pass

    def load_config(self, *args, **kwargs):
        pass

    def load_session(self, *args, **kwargs):
        pass

    def load_plugins(self, *args, **kwargs):
        pass

    async def handle_download(self, *args, **kwargs):
        pass

    async def start(self, *args, **kwargs):
        pass

    async def stop(self, *args, **kwargs):
        pass

    async def connect(self, *args, **kwargs):
        pass

    async def authorize(self, *args, **kwargs):
        pass

    async def disconnect(self, *args, **kwargs):
        pass

    async def initialize(self, *args, **kwargs):
        pass

    async def terminate(self, *args, **kwargs):
        pass
