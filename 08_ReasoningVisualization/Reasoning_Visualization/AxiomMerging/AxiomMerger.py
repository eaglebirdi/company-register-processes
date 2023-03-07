from typing import List
from ..Configuration import Configuration
from ..NamedFile import NamedFile
from ..TPTPProgram import TPTPProgramm

newline = Configuration.newline


class AxiomMerger:
    def __init__(self, merge_into_single_file: bool):
        self.merge_into_single_file = merge_into_single_file

    def create(self, axiom_files: List[NamedFile]) -> TPTPProgramm:
        additional_files = []
        main_program_text = ""

        for axiom_file in axiom_files:
            if self.merge_into_single_file:
                main_program_text += "% ### AXIOM FILE " + axiom_file.name + " ###"
                main_program_text += newline + newline
                main_program_text += axiom_file.content
                main_program_text += newline + newline
            else:
                main_program_text += "include('" + axiom_file.name + "')." + newline
                additional_files.append(NamedFile(axiom_file.name, axiom_file.content))

        result = TPTPProgramm(NamedFile("program.p", main_program_text), additional_files)
        return result
