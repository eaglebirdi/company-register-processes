from typing import List, Union

from .Configuration import Configuration

from .InputData import InputData
from .ProofTreeGeneration.ProofTree.Tree import Tree

from AxiomTextParsing import Parser as TFFParser, TFFAnnotated

from .ProofTreeGeneration.Generator import Generator as ProofTreeGenerator
from .AxiomMerging.AxiomMerger import AxiomMerger
from .LogicProgramsGenerator import LogicProgramsGenerator
from .ProverInvocation.ProofTreeProverInvoker import ProofTreeProverInvoker
from .ProofVisualizer import ProofVisualizer

newline = Configuration.newline


class Executor:
    """
    Logic for executing the whole visualization process.
    """

    def __init__(self, input_data: InputData):
        self.input_data = input_data
        self.proof_tree: Union[Tree, None] = None

    def execute(self) -> None:
        rule_axioms = self._parse_rule_axioms()
        proof_tree_generator = ProofTreeGenerator(rule_axioms)
        proof_tree = proof_tree_generator.generate(self.input_data.root_rule)

        axiom_merger = AxiomMerger(self.input_data.single_file_axioms)
        tptp_program = axiom_merger.create(self.input_data.law_related_axioms + self.input_data.case_related_axioms)

        programs_generator = LogicProgramsGenerator(tptp_program)
        enriched_tree = programs_generator.create(proof_tree, self.input_data.main_object)

        prover_invoker = ProofTreeProverInvoker(self.input_data.prover)
        prover_invoker.execute(enriched_tree)

        self.proof_tree = enriched_tree

    def _parse_rule_axioms(self) -> List[TFFAnnotated]:
        content = ""
        for axiom_file in self.input_data.law_related_axioms:
            content += axiom_file.content + newline + newline

        parser = TFFParser()
        parsed_axioms = parser.parse(content)
        return parsed_axioms

    def print(self) -> None:
        if self.proof_tree is None:
            raise Exception("Execute method must have been called before.")

        visualizer = ProofVisualizer(self.proof_tree)
        visualizer.print()
