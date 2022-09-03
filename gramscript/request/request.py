import time
from datetime import datetime

from ..encode import _no_encode
from ..session import _get_req_session
from ..result import _check_result

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


def _make_request(self, method_name, method='get', params=None, files=None):
    """
    Makes a request to the Telegram API.
    :param token: The bot's API token. (Created with @BotFather)
    :param method_name: Name of the API method to be called. (E.g. 'getUpdates')
    :param method: HTTP method to be used. Defaults to 'get'.
    :param params: Optional parameters. Should be a dictionary with key-value pairs.
    :param files: Optional files.
    :return: The result parsed to a JSON dictionary.
    """
    if not self:
        raise Exception('Bot token is not defined')
    if API_URL:
        # noinspection PyUnresolvedReferences
        request_url = API_URL.format(self, method_name)
    else:
        request_url = "https://api.telegram.org/bot{0}/{1}".format(
            self, method_name)

    logger.debug("Request: method={0} url={1} params={2} files={3}".format(
        method, request_url, params, files).replace(self, self.split(':')[0] + ":{TOKEN}"))

    read_timeout = READ_TIMEOUT
    connect_timeout = CONNECT_TIMEOUT
    if files and format_header_param:
        fields.format_header_param = _no_encode(format_header_param)
    if params:
        if 'timeout' in params:
            read_timeout = params.pop('timeout')
            connect_timeout = read_timeout
#        if 'connect-timeout' in params:
#            connect_timeout = params.pop('connect-timeout') + 10
        if 'long_polling_timeout' in params:
            # For getUpdates: it's the only function with timeout parameter on the BOT API side
            long_polling_timeout = params.pop('long_polling_timeout')
            params['timeout'] = long_polling_timeout
            # Long polling hangs for a given time. Read timeout should be greater that long_polling_timeout
            read_timeout = max(long_polling_timeout + 5, read_timeout)
    # Lets stop suppose that user is stupid and assume that he knows what he do...
    # read_timeout = read_timeout + 10
    # connect_timeout = connect_timeout + 10

    params = params or None  # Set params to None if empty

    result = None
    if RETRY_ON_ERROR and RETRY_ENGINE == 1:
        got_result = False
        current_try = 0
        while not got_result and current_try < MAX_RETRIES-1:
            current_try += 1
            try:
                result = _get_req_session().request(
                    method, request_url, params=params, files=files,
                    timeout=(connect_timeout, read_timeout), proxies=proxy)
                got_result = True
            except HTTPError:
                logger.debug("HTTP Error on {0} method (Try #{1})".format(
                    method_name, current_try))
                time.sleep(RETRY_TIMEOUT)
            except ConnectionError:
                logger.debug("Connection Error on {0} method (Try #{1})".format(
                    method_name, current_try))
                time.sleep(RETRY_TIMEOUT)
            except Timeout:
                logger.debug("Timeout Error on {0} method (Try #{1})".format(
                    method_name, current_try))
                time.sleep(RETRY_TIMEOUT)
        if not got_result:
            result = _get_req_session().request(
                method, request_url, params=params, files=files,
                timeout=(connect_timeout, read_timeout), proxies=proxy)
    elif RETRY_ON_ERROR and RETRY_ENGINE == 2:
        http = _get_req_session()
        retry_strategy = requests.packages.urllib3.retry.Retry(
            total=MAX_RETRIES,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        for prefix in ('http://', 'https://'):
            http.mount(prefix, adapter)
        result = http.request(
            method, request_url, params=params, files=files,
            timeout=(connect_timeout, read_timeout), proxies=proxy)
    elif CUSTOM_REQUEST_SENDER:
        result = CUSTOM_REQUEST_SENDER(
            method, request_url, params=params, files=files,
            timeout=(connect_timeout, read_timeout), proxies=proxy)
    else:
        result = _get_req_session().request(
            method, request_url, params=params, files=files,
            timeout=(connect_timeout, read_timeout), proxies=proxy)

    logger.debug("The server returned: '{0}'".format(
        result.text.encode('utf8')))

    if json_result := _check_result(method_name, result):
        return json_result['result']
