class CaptionParser:

    # Responses #
    class SuccessResponse:
        def __init__(self, effects: list):
            self.is_valid = True
            self.effects = effects

    class ErrorResponse:
        def __init__(self, reply_type, *reply_vars):
            self.is_valid = False
            self.reply_type = reply_type
            self.reply_vars = reply_vars

    # Response Types #
    VAR_AMOUNT = "var-amount"

    # Effect Parser #

    class EffectParser:
        class VarRange:
            def __init__(self, start, end):
                self.start = start
                self.end = end

            def check(self, value):
                return self.start <= value <= self.end

        class VarOptions:
            def __init__(self, options):
                self.options = options

            def check(self, value):
                return value in self.options

        def __init__(self, var_amount_start, var_amount_end, var_list):
            self.var_amount_range = self.VarRange(var_amount_start, var_amount_end)
            self.var_list = var_list

        def parse(self, effect_string):
            command_list = effect_string.strip().split(' ')
            if not self.var_amount_range.check(len(command_list) - 1):
                return CaptionParser.ErrorResponse(CaptionParser.VAR_AMOUNT, [len(command_list) - 1, self.var_amount_range.start, self.var_amount_range.end])


    @staticmethod
    def parse(caption):
