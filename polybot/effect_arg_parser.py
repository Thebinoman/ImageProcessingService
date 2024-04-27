from polybot.effect_arg_rules import ArgRangeRule
from polybot.error import CommandError
from polybot.response_types import ErrorTypes


class EffectArgParser:
    def __init__(self, arg_amount_start: int, arg_amount_end: int, arg_rule_list: iter, multi: bool = False):
        self.arg_amount_range = ArgRangeRule(arg_amount_start, arg_amount_end)
        self.arg_rule_list = arg_rule_list
        self.multi = multi

    def parse(self, arg_list: iter, effect_string: str):
        if type(self.arg_amount_range.parse(len(arg_list), effect_string)) is CommandError:
            return [CommandError(ErrorTypes.ARG_AMOUNT_ERROR, [effect_string, len(arg_list), self.arg_amount_range.start, self.arg_amount_range.end])]

        parsed_args = []
        for i in range(min(len(arg_list), len(self.arg_rule_list))):
            print(arg_list[i], effect_string)
            parsed_args.append(self.arg_rule_list[i].parse(arg_list[i], effect_string))

        return parsed_args
