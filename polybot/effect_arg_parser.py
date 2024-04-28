"""
Effect Arg Parser
A parser for effect commands
"""

# pylint: disable=E0401
from polybot.effect_arg_rules import ArgRangeRule
from polybot.error import CommandError
from polybot.response_types import ErrorTypes
# pylint: enable=E0401


# pylint: disable=R0903
class EffectArgParser:
    """
    Parser for arguments of a command. Each Effect Arg Parser holds:
    1. The range of arguments expected from the user (arg_amount_start and arg_amount_end)
    2. The full list of all its argument rules
    Each argument can have 1 of 4 types of arguments:
    1. Ranged argument, of type ArgRangeRule
    2. Option argument (one value from given options). of type ArgOptionRule
    3. Positive Integer argument, of type ArgPositiveInt
    4. Color argument, of type ArgColorRule
    """

    def __init__(self,
                 arg_amount_start: int,
                 arg_amount_end: int,
                 arg_rule_list: iter,
                 multi: bool = False):
        self.arg_amount_range = ArgRangeRule(arg_amount_start, arg_amount_end)
        self.arg_rule_list = arg_rule_list
        self.multi = multi

    def parse(self, arg_list: iter, effect_string: str):
        """
        Parse the args of a command by a list of given args.
        :param arg_list: Required. List of args as strings.
        :param effect_string: Required. The full command as a string.
        :return: List of parsed values of the arguments, or CommandError instance of error found.
        """

        if isinstance(self.arg_amount_range.parse(len(arg_list), effect_string), CommandError):
            return [
                CommandError(
                    ErrorTypes.ARG_AMOUNT_ERROR,
                    [
                        effect_string, len(arg_list),
                        self.arg_amount_range.start,
                        self.arg_amount_range.end
            ])]

        parsed_args = []
        for i in range(min(len(arg_list), len(self.arg_rule_list))):
            print(arg_list[i], effect_string)
            parsed_args.append(self.arg_rule_list[i].parse(arg_list[i], effect_string))

        return parsed_args
# pylint: enable=R0903
