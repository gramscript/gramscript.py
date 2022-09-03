import time
from datetime import datetime

from ..api import *


try:
    import ujson as json
except ImportError:
    import json

import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout
from requests.adapters import HTTPAdapter

try:
    # noinspection PyUnresolvedReferences
    from requests.packages.urllib3 import fields
    format_header_param = fields.format_header_param
except ImportError:
    format_header_param = None
import gramscript
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


def _no_encode(func):
    def wrapper(key, val):
        return '{0}={1}'.format(key, val) if key == 'filename' else func(key, val)
    return wrapper
