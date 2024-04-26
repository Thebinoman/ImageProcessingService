class Text:
    UNKNOWN = 'unknown'

class Photo:
    PROCESSING = 'processing'
    SEND = 'send'

class DocumentTypes:
    Document = 'document'


class ErrorTypes:
    # Effect Errors #
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
