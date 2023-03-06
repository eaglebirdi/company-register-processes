from typing import List
from .FileResult import FileResult


class GenerationResult:
    def __init__(self,
                 axiom_files: List[FileResult],
                 main_object: str, main_predicate: str):
        self.axiom_files = axiom_files
        self.main_object = main_object
        self.main_predicate = main_predicate
