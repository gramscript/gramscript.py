import filecmp
import io
import sys
import urllib3
import logging
import json
import re
import os

from . import exception

# Suppress InsecurePlatformWarning
urllib3.disable_warnings()


_default_pool_params = dict(num_pools=3, maxsize=10, retries=3, timeout=30)
_onetime_pool_params = dict(num_pools=1, maxsize=1, retries=3, timeout=30)

_pools = {
    'default': urllib3.PoolManager(**_default_pool_params),
}

_onetime_pool_spec = (urllib3.PoolManager, _onetime_pool_params)
PY_3 = sys.version_info.major >= 3
_string_type = str if PY_3 else basestring
_file_type = io.IOBase if PY_3 else filecmp


def _isstring(s):
    return isinstance(s, _string_type)


def _isfile(f):
    return isinstance(f, _file_type)


def set_proxy(url, basic_auth=None):
    """
    Access Bot API through a proxy.

    :param url: proxy URL
    :param basic_auth: 2-tuple ``('username', 'password')``
    """
    global _pools, _onetime_pool_spec
    if not url:
        _pools['default'] = urllib3.PoolManager(**_default_pool_params)
        _onetime_pool_spec = (urllib3.PoolManager, _onetime_pool_params)
    elif basic_auth:
        h = urllib3.make_headers(proxy_basic_auth=':'.join(basic_auth))
        _pools['default'] = urllib3.ProxyManager(
            url, proxy_headers=h, **_default_pool_params)
        _onetime_pool_spec = (urllib3.ProxyManager, dict(
            proxy_url=url, proxy_headers=h, **_onetime_pool_params))
    else:
        _pools['default'] = urllib3.ProxyManager(url, **_default_pool_params)
        _onetime_pool_spec = (urllib3.ProxyManager, dict(
            proxy_url=url, **_onetime_pool_params))


def _create_onetime_pool():
    cls, kw = _onetime_pool_spec
    return cls(**kw)


def _methodurl(req, **user_kw):
    token, method, params, files = req
    return f'https://api.telegram.org/bot{token}/{method}'


def _which_pool(req, **user_kw):
    token, method, params, files = req
    return None if files else 'default'


def _guess_filename(obj):
    name = getattr(obj, 'name', None)
    if name and _isstring(name) and name[0] != '<' and name[-1] != '>':
        return os.path.basename(name)


def _filetuple(key, f):
    if not isinstance(f, tuple):
        return (_guess_filename(f) or key, f.read())
    elif len(f) == 1:
        return (_guess_filename(f[0]) or key, f[0].read())
    elif len(f) == 2:
        return (f[0], f[1].read())
    elif len(f) == 3:
        return (f[0], f[1].read(), f[2])
    else:
        raise ValueError()


PY_3 = sys.version_info.major >= 3


def _fix_type(v):
    return str(v) if isinstance(v, float if PY_3 else (long, float)) else v


def _compose_fields(req, **user_kw):
    token, method, params, files = req
    fields = {k: _fix_type(v) for k, v in params.items()
              } if params is not None else {}

    if files:
        fields |= {k: _filetuple(k, v) for k, v in files.items()}
    return fields


def _default_timeout(req, **user_kw):
    name = _which_pool(req, **user_kw)
    if name is None:
        return _onetime_pool_spec[1]['timeout']
    else:
        return _pools[name].connection_pool_kw['timeout']


def _compose_kwargs(req, **user_kw):
    token, method, params, files = req
    kw = {}
    if not params and not files:
        kw['encode_multipart'] = False
    if method == 'getUpdates' and params and 'timeout' in params:
        kw['timeout'] = params['timeout'] + _default_timeout(req, **user_kw)
    elif files:
        kw['timeout'] = None
    kw |= user_kw
    return kw


def _transform(req, **user_kw):
    kwargs = _compose_kwargs(req, **user_kw)
    fields = _compose_fields(req, **user_kw)
    url = _methodurl(req, **user_kw)
    name = _which_pool(req, **user_kw)
    pool = _create_onetime_pool() if name is None else _pools[name]
    return pool.request_encode_body, ('POST', url, fields), kwargs


def _parse(response):
    try:
        text = response.data.decode('utf-8')
        data = json.loads(text)
    except ValueError as e:
        raise exception.BadHTTPResponse(response.status, text, response) from e
    if data['ok']:
        return data['result']
    description, error_code = data['description'], data['error_code']
    for e in exception.TelegramError.__subclasses__():
        n = len(e.DESCRIPTION_PATTERNS)
        if any(map(re.search, e.DESCRIPTION_PATTERNS, n * [description], n * [re.IGNORECASE])):
            raise e(description, error_code, data)
    raise exception.TelegramError(description, error_code, data)


def request(req, **user_kw):
    fn, args, kwargs = _transform(req, **user_kw)
    r = fn(*args, **kwargs)  # `fn` must be thread-safe
    return _parse(r)


def _fileurl(req):
    token, path = req
    return f'https://api.telegram.org/file/bot{token}/{path}'


def download(req, **user_kw):
    pool = _create_onetime_pool()
    return pool.request('GET', _fileurl(req), **user_kw)
