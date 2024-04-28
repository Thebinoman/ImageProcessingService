"""
Parsing caption of a message into commands,
that can be later be called and executed
"""

# pylint: disable=E0401
from polybot.error import NoCaptionError, CommandError
from polybot.response_types import ErrorTypes
from polybot.effect_rules import EffectRules
# pylint: enable=E0401


# pylint: disable=R0903
class EffectCommand:
    """
    Holds the info of a parsed effect command
    """
    def __init__(self, command_name: str, arg_list: iter, multi: bool = False):
        self.command_name = command_name
        self.arg_list = arg_list
        self.multi = multi


class CaptionParser:
    """
    A static class that parse the caption of a message into EffectCommands
    """

    @staticmethod
    def parse(caption: str):
        """
        Parse the caption into EffectCommand or CommandError instances
        :param caption: Required. The given caption as a string.
        :return: List of commands as EffectCommands or CommandErrors
        """
        # Strip spaces from the beginning and the end
        caption = caption.strip()
        # If the caption is empty, return no caption error
        if not caption:
            return [NoCaptionError]
        # Split to commands
        effect_list = caption.split(',')

        # Create the list for the results
        commands = []
        # Iterate over all commands
        for effect_string in effect_list:
            # Strip spaces from the beginning and the end
            effect_string = effect_string.strip()
            # Split the arguments of the commands
            effect_args = effect_string.split(' ')
            # Extract the effect name as inserted as input
            effect_name_input = effect_args.pop(0).strip()
            # Parse the effect name to match the method names
            # in Img class and the reply system
            effect_name = effect_name_input.replace('-', '_')

            # If effect name is not found, add Effect Not Found error
            if effect_name not in EffectRules:
                commands.append(CommandError(ErrorTypes.EFFECT_NOT_FOUND, [effect_name_input]))
            # If effect name exists
            else:
                # Fetch it's arg parser
                effect_arg_parser = EffectRules[effect_name]
                # Parse the args with its parser, and add it to the results
                commands.append(
                    EffectCommand(
                        effect_name,
                        effect_arg_parser.parse(
                            effect_args, effect_string),
                        effect_arg_parser.multi
                ))

        return commands
# pylint: enable=R0903
