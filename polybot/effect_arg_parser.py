from polybot.effect_arg_rules import ArgRangeRule
from polybot.error import CommandError
from polybot.response_types import ErrorTypes


class EffectArgParser:
    def __init__(self, arg_amount_start: int, arg_amount_end: int, arg_rule_list: iter, multi: bool = False):
        self.arg_amount_range = ArgRangeRule(arg_amount_start, arg_amount_end)
        self.arg_rule_list = arg_rule_list
        self.multi = multi

    def parse(self, arg_list: iter, effect_string: str):
        if self.arg_amount_range.parse(len(arg_list), effect_string) is CommandError:
            return [CommandError(ErrorTypes.ARG_AMOUNT_ERROR, [effect_string, len(arg_list), self.arg_amount_range.start, self.arg_amount_range.end])]

        return list(map(lambda arg_string, arg_rule: arg_rule.parse(arg_string, effect_string), arg_list, self.arg_rule_list))
