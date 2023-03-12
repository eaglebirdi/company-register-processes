from typing import Tuple, Union
from .ProverResult import ProverResult


class IProverTool:
    SZS_prefix = "% SZS status "

    def __init__(self):
        pass

    """
    Executes the prover for the passed program file.
    """
    def execute(self, program_file_path: str) -> ProverResult:
        pass

    def _get_szs_status_line(self, output_lines) -> Tuple[Union[str, None], int]:
        status_line_indices = [i for i in range(0, len(output_lines)) if output_lines[i].startswith(self.SZS_prefix)]
        if len(status_line_indices) != 1:
            return "", -1

        status_line_index = status_line_indices[0]
        status_line = output_lines[status_line_index]
        return status_line, status_line_index
