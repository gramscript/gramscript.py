try:
    import ujson as json
except ImportError:
    import json
from gramscript import util


class JsonSerializable(object):
    """
    Subclasses of this class are guaranteed to be able to be converted to JSON format.
    All subclasses of this class must override to_json.
    """

    def to_json(self):
        """
        Returns a JSON string representation of this class.

        This function must be overridden by subclasses.
        :return: a JSON formatted string.
        """
        raise NotImplementedError


class Dictionaryable(object):
    """
    Subclasses of this class are guaranteed to be able to be converted to dictionary.
    All subclasses of this class must override to_dict.
    """

    def to_dict(self):
        """
        Returns a DICT with class field values

        This function must be overridden by subclasses.
        :return: a DICT
        """
        raise NotImplementedError


class JsonDeserializable(object):
    """
    Subclasses of this class are guaranteed to be able to be created from a json-style dict or json formatted string.
    All subclasses of this class must override de_json.
    """

    @classmethod
    def de_json(cls, json_string):
        """
        Returns an instance of this class from the given json dict or string.

        This function must be overridden by subclasses.
        :return: an instance of this class created from the given json dict or string.
        """
        raise NotImplementedError

    @staticmethod
    def check_json(json_type, dict_copy=True):
        """
        Checks whether json_type is a dict or a string. If it is already a dict, it is returned as-is.
        If it is not, it is converted to a dict by means of json.loads(json_type)
        :param json_type: input json or parsed dict
        :param dict_copy: if dict is passed and it is changed outside - should be True!
        :return: Dictionary parsed from json or original dict
        """
        if util.is_dict(json_type):
            return json_type.copy() if dict_copy else json_type
        elif util.is_string(json_type):
            return json.loads(json_type)
        else:
            raise ValueError("json_type should be a json dict or string.")

    def __str__(self):
        d = {
            x: y.__dict__ if hasattr(y, '__dict__') else y
            for x, y in self.__dict__.items()
        }
        return str(d)


class LoginUrl(Dictionaryable, JsonSerializable, JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string, dict_copy=False)
        return cls(**obj)

    def __init__(self, url, forward_text=None, bot_username=None, request_write_access=None, **kwargs):
        self.url: str = url
        self.forward_text: str = forward_text
        self.bot_username: str = bot_username
        self.request_write_access: bool = request_write_access

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        json_dict = {'url': self.url}
        if self.forward_text:
            json_dict['forward_text'] = self.forward_text
        if self.bot_username:
            json_dict['bot_username'] = self.bot_username
        if self.request_write_access is not None:
            json_dict['request_write_access'] = self.request_write_access
        return json_dict
