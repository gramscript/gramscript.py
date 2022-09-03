try:
    import ujson as json
except ImportError:
    import json

from ..api import ApiHTTPException
from ..session import _get_req_session
from ..request import _make_request

FILE_URL = None
proxy = None
# Should be positive, short polling should be used for testing purposes only (https://core.telegram.org/bots/api#getupdates)
LONG_POLLING_TIMEOUT = 10


def get_file(token, file_id):
    method_url = r'getFile'
    return _make_request(token, method_url, params={'file_id': file_id})


def get_file_url(token, file_id):
    if FILE_URL is None:
        return "https://api.telegram.org/file/bot{0}/{1}".format(token, get_file(token, file_id)['file_path'])
    else:
        # noinspection PyUnresolvedReferences
        return FILE_URL.format(token, get_file(token, file_id)['file_path'])


def download_file(token, file_path):
    if FILE_URL is None:
        url = "https://api.telegram.org/file/bot{0}/{1}".format(
            token, file_path)
    else:
        # noinspection PyUnresolvedReferences
        url = FILE_URL.format(token, file_path)

    result = _get_req_session().get(url, proxies=proxy)
    if result.status_code != 200:
        raise ApiHTTPException('Download file', result)

    return result.content


def get_me(token):
    method_url = r'getMe'
    return _make_request(token, method_url)


def log_out(token):
    method_url = r'logOut'
    return _make_request(token, method_url)


def close(token):
    method_url = r'close'
    return _make_request(token, method_url)


def get_updates(token, offset=None, limit=None, timeout=None, allowed_updates=None, long_polling_timeout=None):
    method_url = 'getUpdates'
    payload = {}
    if offset:
        payload['offset'] = offset
    if limit:
        payload['limit'] = limit
    if timeout:
        payload['timeout'] = timeout
    payload['long_polling_timeout'] = long_polling_timeout or LONG_POLLING_TIMEOUT
    if allowed_updates is not None:
        payload['allowed_updates'] = json.dumps(allowed_updates)
    return _make_request(token, method_url, params=payload)
