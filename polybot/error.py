from typing import Union
from polybot.response_types import ErrorTypes


class NoCaptionError:
    error_type = ErrorTypes.NO_CAPTION


class CommandError:
    def __init__(self, error_type: Union[str, property], error_args: iter):
        self.error_type = error_type
        self.error_args = error_args

