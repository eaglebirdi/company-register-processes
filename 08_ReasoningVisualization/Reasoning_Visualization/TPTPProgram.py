from typing import List
from .NamedFile import NamedFile


class TPTPProgram:
    def __init__(self, main_program: NamedFile, additional_files: List[NamedFile]):
        self.main_program = main_program
        self.additional_files = additional_files
