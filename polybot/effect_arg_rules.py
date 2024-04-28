"""
Rules of parsing arguments of an effect command
"""

import json
from typing import Union
from PIL import ImageColor
# pylint: disable=E0401
from polybot.response_types import ErrorTypes
from polybot.caption_parser import CommandError
# pylint: enable=E0401

with open(
        'polybot/replies/Image_processing_bot_replies.json',
        encoding="utf-8"
) as replies_file:
    replies = json.loads(replies_file.read())


# pylint: disable=R0903
class ArgRuleBase:
    """
    Argument Rules Base. All argument rules classes are inheriting from this class.
    """

    # pylint: disable=W0613
    def parse(self, value: Union[str, int], effect_string: str):
        """
        Parse the given value or return a CommandError

        :param value: Required. The value be parsed.
        :param effect_string: Required. The original string of the full effect command.
        :return: The parsed value, or CommandError if value cannot be parsed.
        """

        return value
    # pylint: enable=W0613


class ArgRangeRule(ArgRuleBase):
    """
    Rules for parsing a range argument
    """
    def __init__(self, start, end, convert_func = int):
        self.start = start
        self.end = end
        self.convert_func = convert_func

    def parse(self, value: Union[str, int], effect_string: str):
        """
        Parse the given value or return a CommandError

        :param value: Required. The value be parsed.
        :param effect_string: Required. The original string of the full effect command.
        :return: An integer within the range, or CommandError if error was found.
        """

        # Try converting the value
        if self.convert_func:
            try:
                value = self.convert_func(value)

            # If failed, return error
            except (ValueError, TypeError):
                return CommandError(
                    ErrorTypes.ARG_WRONG_TYPE,
                    [
                        effect_string,
                        value
                ])

        # If value is in range, return the value
        if self.start <= value <= self.end:
            return value

        # Else if the range has more then one option, return an out of range error
        if self.start != self.end:
            error_type = ErrorTypes.ARG_OUT_OF_RANGE
        # Else return a set to error
        else:
            error_type = ErrorTypes.ARG_SET_TO
        return CommandError(
            error_type,
            [
                effect_string,
                self.start,
                self.end,
                value
        ])


class ArgOptionRule(ArgRuleBase):
    """
    Rules for parsing an Option argument
    """

    def __init__(self, options: iter, convert_func = None):
        self.options = options
        self.convert_func = convert_func

    def parse(self, value: str, effect_string: str):
        """
        Parse the given value or return a CommandError

        :param value: Required. The value be parsed.
        :param effect_string: Required. The original string of the full effect command.
        :return: The selected option by the value, or CommandError if error was found
        """

        # Try converting the value
        if self.convert_func:
            try:
                value = self.convert_func(value)

            # If failed, return error
            except (ValueError, TypeError):
                return CommandError(
                    ErrorTypes.ARG_WRONG_TYPE,
                    [
                        effect_string,
                        value
                    ])

        # If value is in the given option, return the value
        if value in self.options:
            return value

        # Else, return an error saying the value not in options
        return CommandError(
            ErrorTypes.ARG_NOT_IN_OPTION,
            [
                effect_string,
                self.options,
                value
        ])


class ArgPositiveInt(ArgRuleBase):
    """
    Rules for Parsing a positive integer
    """

    def parse(self, value: str, effect_string: str):
        """
        Parse the given value or return a CommandError

        :param value: Required. The value be parsed.
        :param effect_string: Required. The original string of the full effect command.
        :return: The parse positive integer, or CommandError if an error found.
        """

        # Try to convert the value to int
        try:
            value = int(value)

        # If failed, return error
        except (ValueError, TypeError):
            return CommandError(
                ErrorTypes.ARG_POSITIVE_INT,
                [
                    effect_string,
                    value
            ])

        # If negative, return error
        if value < 0:
            return CommandError(
                ErrorTypes.ARG_POSITIVE_INT,
                [
                    effect_string,
                    value
            ])

        # Else, return the parsed value
        return value


class ArgColorRule(ArgRuleBase):
    """
    Rules for parsing a color argument
    """
    def parse(self, value: str, effect_string: str):
        """
        Parse the given value or return a CommandError

        :param value: Required. The color value to be parsed.
        :param effect_string: Required. The original string of the full effect command.
        :return: A tuple of RGB values, or CommandError if cannot be parsed
        """

        # try to convert to RGB
        try:
            value = ImageColor.getrgb(value)

        # return CommandError if not convertable
        except ValueError:
            return CommandError(
                ErrorTypes.ARG_NOT_COLOR,
                [
                    effect_string,
                    value
            ])

        return value
    # pylint: enable=R0903
