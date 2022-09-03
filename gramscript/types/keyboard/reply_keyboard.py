import logging
from typing import Dict, List, Optional, Union

from types import JsonSerializable, KeyboardButton

try:
    import ujson as json
except ImportError:
    import json

DISABLE_KEYLEN_ERROR = False

logger = logging.getLogger('gramscript')


class ReplyKeyboardRemove(JsonSerializable):
    def __init__(self, selective=None):
        self.selective: bool = selective

    def to_json(self):
        json_dict = {'remove_keyboard': True}
        if self.selective:
            json_dict['selective'] = self.selective
        return json.dumps(json_dict)


class ReplyKeyboardMarkup(JsonSerializable):
    max_row_keys = 12

    def __init__(self, resize_keyboard: Optional[bool] = None, one_time_keyboard: Optional[bool] = None,
                 selective: Optional[bool] = None, row_width: int = 3, input_field_placeholder: Optional[str] = None):
        if row_width > self.max_row_keys:
            # Todo: Will be replaced with Exception in future releases
            if not DISABLE_KEYLEN_ERROR:
                logger.error(
                    'Telegram does not support reply keyboard row width over %d.' % self.max_row_keys)
            row_width = self.max_row_keys

        self.resize_keyboard: bool = resize_keyboard
        self.one_time_keyboard: bool = one_time_keyboard
        self.selective: bool = selective
        self.row_width: int = row_width
        self.input_field_placeholder: str = input_field_placeholder
        self.keyboard: List[List[KeyboardButton]] = []

    def add(self, *args, row_width=None):
        """
        This function adds strings to the keyboard, while not exceeding row_width.
        E.g. ReplyKeyboardMarkup#add("A", "B", "C") yields the json result {keyboard: [["A"], ["B"], ["C"]]}
        when row_width is set to 1.
        When row_width is set to 2, the following is the result of this function: {keyboard: [["A", "B"], ["C"]]}
        See https://core.telegram.org/bots/api#replykeyboardmarkup
        :param args: KeyboardButton to append to the keyboard
        :param row_width: width of row
        :return: self, to allow function chaining.
        """
        if row_width is None:
            row_width = self.row_width

        if row_width > self.max_row_keys:
            # Todo: Will be replaced with Exception in future releases
            if not DISABLE_KEYLEN_ERROR:
                logger.error(
                    'Telegram does not support reply keyboard row width over %d.' % self.max_row_keys)
            row_width = self.max_row_keys

        for row in chunks(args, row_width):
            button_array = []
            for button in row:
                if is_string(button):
                    button_array.append({'text': button})
                elif is_bytes(button):
                    button_array.append({'text': button.decode('utf-8')})
                else:
                    button_array.append(button.to_dict())
            self.keyboard.append(button_array)

        return self

    def row(self, *args):
        """
        Adds a list of KeyboardButton to the keyboard. This function does not consider row_width.
        ReplyKeyboardMarkup#row("A")#row("B", "C")#to_json() outputs '{keyboard: [["A"], ["B", "C"]]}'
        See https://core.telegram.org/bots/api#replykeyboardmarkup
        :param args: strings
        :return: self, to allow function chaining.
        """

        return self.add(*args, row_width=self.max_row_keys)

    def to_json(self):
        """
        Converts this object to its json representation following the Telegram API guidelines described here:
        https://core.telegram.org/bots/api#replykeyboardmarkup
        :return:
        """
        json_dict = {'keyboard': self.keyboard}
        if self.one_time_keyboard is not None:
            json_dict['one_time_keyboard'] = self.one_time_keyboard
        if self.resize_keyboard is not None:
            json_dict['resize_keyboard'] = self.resize_keyboard
        if self.selective is not None:
            json_dict['selective'] = self.selective
        if self.input_field_placeholder:
            json_dict['input_field_placeholder'] = self.input_field_placeholder
        return json.dumps(json_dict)
