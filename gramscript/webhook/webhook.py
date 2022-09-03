try:
    import ujson as json
except ImportError:
    import json

from gramscript.request import _make_request


def set_webhook(token, url=None, certificate=None, max_connections=None, allowed_updates=None, ip_address=None, drop_pending_updates=None, timeout=None):
    method_url = 'setWebhook'
    payload = {'url': url or ""}
    files = {'certificate': certificate} if certificate else None
    if max_connections:
        payload['max_connections'] = max_connections
    if allowed_updates is not None:
        payload['allowed_updates'] = json.dumps(allowed_updates)
    if ip_address is not None:
        payload['ip_address'] = ip_address
    if drop_pending_updates is not None:
        payload['drop_pending_updates'] = drop_pending_updates
    if timeout:
        payload['timeout'] = timeout
    return _make_request(token, method_url, params=payload, files=files)


def delete_webhook(token, drop_pending_updates=None, timeout=None):
    method_url = r'deleteWebhook'
    payload = {}
    if drop_pending_updates is not None:  # Any bool value should pass
        payload['drop_pending_updates'] = drop_pending_updates
    if timeout:
        payload['timeout'] = timeout
    return _make_request(token, method_url, params=payload)


def get_webhook_info(token, timeout=None):
    method_url = r'getWebhookInfo'
    payload = {}
    if timeout:
        payload['timeout'] = timeout
    return _make_request(token, method_url, params=payload)
