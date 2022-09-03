try:
    import ujson as json
except ImportError:
    import json
import logging
from typing import List

from gramscript import util

from ..object import Dictionaryable, JsonDeserializable, JsonSerializable
from .keyboard_button import InlineKeyboardButton

logger = logging.getLogger('gramscript')


class InlineKeyboardMarkup(Dictionaryable, JsonSerializable, JsonDeserializable):
    max_row_keys = 8

    @classmethod
    def de_json(cls, json_string):
        if json_string is None:
            return None
        obj = cls.check_json(json_string, dict_copy=False)
        keyboard = [[InlineKeyboardButton.de_json(
            button) for button in row] for row in obj['inline_keyboard']]
        return cls(keyboard=keyboard)

    def __init__(self, keyboard=None, row_width=3):
        """
        This object represents an inline keyboard that appears
            right next to the message it belongs to.

        :return:
        """
        if row_width > self.max_row_keys:
            # Todo: Will be replaced with Exception in future releases
            logger.error(
                'Telegram does not support inline keyboard row width over %d.' % self.max_row_keys)
            row_width = self.max_row_keys

        self.row_width: int = row_width
        self.keyboard: List[List[InlineKeyboardButton]] = keyboard or []

    def add(self, *args, row_width=None):
        """
        This method adds buttons to the keyboard without exceeding row_width.

        E.g. InlineKeyboardMarkup.add("A", "B", "C") yields the json result:
            {keyboard: [["A"], ["B"], ["C"]]}
        when row_width is set to 1.
        When row_width is set to 2, the result:
            {keyboard: [["A", "B"], ["C"]]}
        See https://core.telegram.org/bots/api#inlinekeyboardmarkup

        :param args: Array of InlineKeyboardButton to append to the keyboard
        :param row_width: width of row
        :return: self, to allow function chaining.
        """
        if row_width is None:
            row_width = self.row_width
        if row_width > self.max_row_keys:
            logger.error(
                'Telegram does not support inline keyboard row width over %d.' % self.max_row_keys)

            row_width = self.max_row_keys
        for row in chunks(args, row_width):
            button_array = list(row)
            self.keyboard.append(button_array)
        return self

    def row(self, *args):
        """
        Adds a list of InlineKeyboardButton to the keyboard.
            This method does not consider row_width.

        InlineKeyboardMarkup.row("A").row("B", "C").to_json() outputs:
            '{keyboard: [["A"], ["B", "C"]]}'
        See https://core.telegram.org/bots/api#inlinekeyboardmarkup

        :param args: Array of InlineKeyboardButton to append to the keyboard
        :return: self, to allow function chaining.
        """

        return self.add(*args, row_width=self.max_row_keys)

    def to_json(self):
        """
        Converts this object to its json representation
            following the Telegram API guidelines described here:
        https://core.telegram.org/bots/api#inlinekeyboardmarkup
        :return:
        """
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {'inline_keyboard': [[button.to_dict() for button in row] for row in self.keyboard]}
