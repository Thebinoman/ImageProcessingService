"""
Commonly used errors in this app
"""

# pylint: disable=E0401
from typing import Union
from polybot.response_types import ErrorTypes
# pylint: enable=E0401


# pylint: disable=R0903
class NoCaptionError:
    """
    No Caption Error. Holds the error_type of 'no-caption'
    """

    error_type = ErrorTypes.NO_CAPTION


class CommandError:
    """
    Cover all cases of error in am effect command or its arguments
    """

    def __init__(self, error_type: Union[str, property], error_args: iter):
        self.error_type = error_type
        self.error_args = error_args
# pylint: enable=R0903
