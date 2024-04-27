from typing import Union
import json
from PIL import ImageColor
from polybot.response_types import ErrorTypes
from polybot.caption_parser import CommandError

with open('polybot/reply_templates/Image_processing_bot_replies.json') as replies_file:
    replies = json.loads(replies_file.read())


class ArgRuleBase:
    def parse(self, value: Union[str, int], effect_string: str):
        return value


class ArgRangeRule(ArgRuleBase):
    def __init__(self, start, end, convert_func = int):
        self.start = start
        self.end = end
        self.convert_func = convert_func

    def parse(self, value: Union[str, int], effect_string: str):
        if self.convert_func:
            try:
                value = self.convert_func(value)
            except (ValueError, TypeError) as error:
                return CommandError(
                    ErrorTypes.ARG_WRONG_TYPE,
                    [
                        effect_string,
                        value
                ])

        if self.start <= value <= self.end:
            return value
        else:
            if self.start != self.end:
                error_type = ErrorTypes.ARG_OUT_OF_RANGE
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
    def __init__(self, options: iter, convert_func = None):
        self.options = options
        self.convert_func = convert_func

    def parse(self, value: str, effect_string: str):
        if self.convert_func:
            try:
                value = self.convert_func(value)
            except (ValueError, TypeError):
                return CommandError(
                    ErrorTypes.ARG_WRONG_TYPE,
                    [
                        effect_string,
                        value
                    ])

        if value in self.options:
            return value
        else:
            return CommandError(
                ErrorTypes.ARG_NOT_IN_OPTION,
                [
                    effect_string,
                    self.options,
                    value
            ])


class ArgPositiveInt(ArgRuleBase):
    def parse(self, value: str, effect_string: str):
        try:
            value = int(value)
        except (ValueError, TypeError) as error:
            return CommandError(
                ErrorTypes.ARG_POSITIVE_INT,
                [
                    effect_string,
                    value
            ])
        if value < 0:
            return CommandError(
                ErrorTypes.ARG_POSITIVE_INT,
                [
                    effect_string,
                    value
            ])
        else:
            return value


class ArgColorRule(ArgRuleBase):
    def parse(self, value: str, effect_string: str):
        try:
            value = ImageColor.getrgb(value)
        except ValueError:
            return CommandError(
                ErrorTypes.ARG_NOT_COLOR,
                [
                    effect_string,
                    value
            ])

        return value
