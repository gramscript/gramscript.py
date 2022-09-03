# -*- coding: utf-8 -*-
import time
from datetime import datetime

import gramscript

try:
    import ujson as json
except ImportError:
    import json

import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout
from requests.adapters import HTTPAdapter

from gramscript import util

logger = gramscript.logger

proxy = None
session = None

API_URL = None
FILE_URL = None

CONNECT_TIMEOUT = 15
READ_TIMEOUT = 30

# Should be positive, short polling should be used for testing purposes only (https://core.telegram.org/bots/api#getupdates)
LONG_POLLING_TIMEOUT = 10

SESSION_TIME_TO_LIVE = 600  # In seconds. None - live forever, 0 - one-time

RETRY_ON_ERROR = False
RETRY_TIMEOUT = 2
MAX_RETRIES = 15
RETRY_ENGINE = 1

CUSTOM_SERIALIZER = None
CUSTOM_REQUEST_SENDER = None

ENABLE_MIDDLEWARE = False


def _get_req_session(reset=False):
    if SESSION_TIME_TO_LIVE:
        creation_date = per_thread(
            'req_session_time', lambda: datetime.now(), reset)

        if (datetime.now() - creation_date).total_seconds() > SESSION_TIME_TO_LIVE:
            reset = True
            per_thread('req_session_time', lambda: datetime.now(), True)
    if SESSION_TIME_TO_LIVE == 0:
        return requests.sessions.Session()
    else:
        return per_thread('req_session', lambda: session or requests.sessions.Session(), reset)
