import os
import subprocess
from .IProverTool import IProverTool
from .ProverResult import ProverResult
from .ProverResultType import ProverResultType


class VampireProver(IProverTool):
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
            "vampire",
            "-t",
            str(self.timeout_in_seconds),
            "-p",
            "off",
            program_file_name
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=program_file_directory)
        out, err = pipe.communicate()
        output = out.decode('utf-8')
        error = err.decode('utf-8')
        return error if output == '' else output

    def _parse_output(self, output_text):
        output_lines = output_text.splitlines()

        if len(output_lines) == 0:
            return ProverResult(ProverResultType.UNEXPECTED_OUTPUT, output_text)

        first_line = output_lines[0]
        if first_line.startswith("User error: Cannot open problem file: "):
            return ProverResult(ProverResultType.FILE_NOT_FOUND, output_text)

        if "% Failed with" in output_lines:
            return ProverResult(ProverResultType.INPUT_ERROR, output_text)

        szs_status_line, szs_status_idx = self._get_szs_status_line(output_lines)

        if szs_status_idx == -1:
            if "% Termination reason: Time limit" in output_lines:
                return ProverResult(ProverResultType.TIMEOUT, output_text)
            else:
                return ProverResult(ProverResultType.UNEXPECTED_OUTPUT, output_text)

        if szs_status_line.startswith(self.SZS_prefix + "Theorem"):
            return ProverResult(ProverResultType.VALID, output_text)
        elif szs_status_line.startswith(self.SZS_prefix + "CounterSatisfiable"):
            return ProverResult(ProverResultType.FALSIFIABLE, output_text)
        elif szs_status_line.startswith(self.SZS_prefix + "ContradictoryAxioms"):
            return ProverResult(ProverResultType.CONTRADICTION, output_text)
        else:
            return ProverResult(ProverResultType.UNEXPECTED_OUTPUT, output_text)
