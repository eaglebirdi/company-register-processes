from typing import List
from .NamedFile import NamedFile
from .ProverTools.IProverTool import IProverTool


class InputData:
    def __init__(self, law_related_axiom: List[NamedFile], case_related_axioms: List[NamedFile],
                 root_rule: str, main_object: str, prover: IProverTool,
                 single_file_axioms: bool = False):
        self.law_related_axioms = law_related_axiom
        self.case_related_axioms = case_related_axioms
        self.root_rule = root_rule
        self.main_object = main_object
        self.prover = prover
        self.single_file_axioms = single_file_axioms
