from .ProverResultType import ProverResultType


class ProverResult:
    def __init__(self, result_type: ProverResultType, full_output: str):
        self.result_type = result_type
        self.full_output = full_output
