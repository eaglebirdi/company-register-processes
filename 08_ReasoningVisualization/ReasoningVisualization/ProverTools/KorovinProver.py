import os
import subprocess
from .IProverTool import IProverTool
from .ProverResult import ProverResult
from .ProverResultType import ProverResultType


class KorovinProver(IProverTool):
    def __init__(self, timeout_in_seconds: int):
        super().__init__()
        self.timeout_in_seconds = timeout_in_seconds

    def execute(self, program_file_path: str) -> ProverResult:
        path, file_name = os.path.split(program_file_path)
        output = self._exec_and_get_output(file_name, path)
        result = self._parse_output(output)
        return result

    def _exec_and_get_output(self, program_file_name, program_file_directory) -> str:
        pipe = subprocess.Popen([
            "iProver",
            "--time_out_real",
            str(self.timeout_in_seconds),
            "--stats_out",
            "none",
            "--out_options",
            "none",
            program_file_name
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=program_file_directory)
        out, err = pipe.communicate()
        output = out.decode('utf-8')
        error = err.decode('utf-8')

        result = output + "\n" + error
        return result

    def _parse_output(self, output_text):
        output_lines = output_text.splitlines()

        if len(output_lines) == 0:
            return ProverResult(ProverResultType.UNEXPECTED_OUTPUT, output_text)

        szs_status_line, szs_status_idx = self._get_szs_status_line(output_lines)

        if szs_status_idx == -1:
            return ProverResult(ProverResultType.UNEXPECTED_OUTPUT, output_text)

        if "Unknown for " in szs_status_line:
            fatal_error = [x for x in output_lines if "Fatal error: exception" in x]

            if len(fatal_error) > 0:
                if "No such file or directory" in fatal_error[0]:
                    return ProverResult(ProverResultType.FILE_NOT_FOUND, output_text)
                else:
                    return ProverResult(ProverResultType.INPUT_ERROR, output_text)
            else:
                time_out = [x for x in output_lines if "Time Out Real" in x]
                if len(time_out) > 0:
                    return ProverResult(ProverResultType.TIMEOUT, output_text)

            return ProverResult(ProverResultType.UNEXPECTED_OUTPUT, output_text)
        elif " Theorem for " in szs_status_line:
            return ProverResult(ProverResultType.VALID, output_text)
        elif " Satisfiable for " in szs_status_line:
            return ProverResult(ProverResultType.FALSIFIABLE, output_text)
        elif " CounterSatisfiable for " in szs_status_line:
            return ProverResult(ProverResultType.FALSIFIABLE, output_text)
        else:
            return ProverResult(ProverResultType.UNEXPECTED_OUTPUT, output_text)
