from gramscript.types import JsonSerializable


class WebhookInfo(JsonSerializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string, dict_copy=False)
        return cls(**obj)

    def __init__(self, url, has_custom_certificate, pending_update_count, ip_address=None,
                 last_error_date=None, last_error_message=None, max_connections=None,
                 allowed_updates=None, **kwargs):
        self.url = url
        self.has_custom_certificate = has_custom_certificate
        self.pending_update_count = pending_update_count
        self.ip_address = ip_address
        self.last_error_date = last_error_date
        self.last_error_message = last_error_message
        self.max_connections = max_connections
        self.allowed_updates = allowed_updates
