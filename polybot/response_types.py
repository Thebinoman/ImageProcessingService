"""
All response types used in this app.
The values should be identical to the keys used in the reply file
"""


# pylint: disable=R0903
class Text:
    """
    All text response types
    """
    UNKNOWN = 'unknown'

class Photo:
    """
    All photo response types
    """

    PROCESSING = 'processing'
    SEND = 'send'

class DocumentTypes:
    """
    All document response types
    """

    Document = 'document'


class Help:
    """
    All help response types
    """

    UNKNOWN = 'unknown'
    HELP = 'help'


class ErrorTypes:
    """
    All error response types
    """

    NO_CAPTION = 'no-caption'
    EFFECT_NOT_FOUND = 'effect-not-found'
    TOO_MUCH_MULTI_IMAGE = 'to-much-multi-image'
    NO_2ND_IMAGE = 'no-2nd-image'
    ARG_AMOUNT_ERROR = 'arg-amount'
    ARG_ERROR = 'arg-error'
    ARG_WRONG_TYPE = 'arg-wrong-type'
    ARG_OUT_OF_RANGE = 'arg-out-of-range'
    ARG_SET_TO = 'arg-set-to'
    ARG_NOT_IN_OPTION = 'arg-not-in-option'
    ARG_NOT_COLOR = 'arg-not-color'
    ARG_POSITIVE_INT = 'arg-not-positive-int'
    ENDING = 'error-ending'
# pylint: enable=R0903
