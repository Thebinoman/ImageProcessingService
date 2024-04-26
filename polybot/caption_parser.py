from polybot.error import NoCaptionError, CommandError
from polybot.response_types import ErrorTypes
from polybot.effect_arg_rules import ArgRangeRule
from polybot.effect_rules import EffectRules


class EffectCommand:
    def __init__(self, command_name: str, arg_list: iter, multi: bool = False):
        self.command_name = command_name
        self.arg_list = arg_list
        self.multi = multi


class CaptionParser:
    @staticmethod
    def parse(caption: str):
        caption = caption.strip()
        if not caption:
            return [NoCaptionError]
        effect_list = caption.split(',')

        commands = []
        for effect_string in effect_list:
            effect_string = effect_string.strip()
            effect_args = effect_string.split(' ')
            effect_name_input = effect_args.pop(0).strip()
            effect_name = effect_name_input.replace('-', '_')

            if effect_name not in EffectRules:
                commands.append(CommandError(ErrorTypes.EFFECT_NOT_FOUND, [effect_name_input]))
            else:
                effect_arg_parser = EffectRules[effect_name]
                commands.append(EffectCommand(effect_name, effect_arg_parser.parse(effect_args, effect_string), effect_arg_parser.multi))

        return commands
