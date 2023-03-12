import os
import shutil
import uuid
from ..TPTPProgram import TPTPProgram
from ..ProverTools.IProverTool import IProverTool
from ..ProverTools.ProverResult import ProverResult
from ..ProverTools.ProverResultType import ProverResultType


class ProverInvoker:
    """
    Logic for invoking the prover tool and organizing the file system accesses.
    """

    def __init__(self, prover_tool: IProverTool):
        self.prover_tool = prover_tool

    def execute(self, tptp_program: TPTPProgram) -> ProverResult:
        program_id = self._create_program_id()
        folder_path = self._create_program_folder(program_id)

        for axiom_file in tptp_program.additional_files:
            self._write_file(folder_path, axiom_file.name, axiom_file.content)

        main_program = tptp_program.main_program
        main_program_path = self._write_file(folder_path, main_program.name, main_program.content)

        result = self.prover_tool.execute(main_program_path)

        if result.result_type not in [ProverResultType.VALID, ProverResultType.FALSIFIABLE]:
            print(str(result.result_type) + ": " + result.full_output)

        self._delete_program_folder(folder_path)

        return result

    def _create_program_id(self):
        program_id = "_" + uuid.uuid4().hex
        return program_id

    def _create_program_folder(self, program_id: str):
        folder_path = "./" + program_id
        os.mkdir(folder_path)
        return folder_path

    def _write_file(self, folder_path: str, file_name: str, file_content: str) -> str:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'w') as fi:
            fi.write(file_content)
        return file_path

    def _delete_program_folder(self, folder_path: str):
        shutil.rmtree("./" + folder_path)
