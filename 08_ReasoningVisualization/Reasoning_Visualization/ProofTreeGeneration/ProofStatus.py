from enum import Enum


class ProofStatus(Enum):
    PROVED = 1
    NOT_PROVED = 0
    ERROR = -1
    TIMEOUT = -2
