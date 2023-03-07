from enum import Enum


class ProverResultType(Enum):
    VALID = 0
    FALSIFIABLE = 1
    CONTRADICTION = 2
    UNEXPECTED_OUTPUT = -1
    TIMEOUT = -2
    INPUT_ERROR = -3
    FILE_NOT_FOUND = -4
