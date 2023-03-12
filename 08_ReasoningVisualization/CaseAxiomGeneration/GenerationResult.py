from typing import List
from ReasoningVisualization import NamedFile


class GenerationResult:
    def __init__(self,
                 axiom_files: List[NamedFile],
                 main_object: str, main_predicate: str):
        self.axiom_files = axiom_files
        self.main_object = main_object
        self.main_predicate = main_predicate
