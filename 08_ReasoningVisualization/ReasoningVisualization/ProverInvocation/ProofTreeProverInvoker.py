from ..ProofTreeGeneration.ProofTree.Tree import Tree
from ..ProofTreeGeneration.ProofTree.Item import Item
from ..ProofTreeGeneration.ProofTree.EnrichedItem import EnrichedItem
from ..ProofTreeGeneration.ProofTree.ProofStatus import ProofStatus
from ..ProverTools.IProverTool import IProverTool
from ..ProverTools.ProverResult import ProverResult
from ..ProverTools.ProverResultType import ProverResultType
from .ProverInvoker import ProverInvoker


class ProofTreeProverInvoker:
    """
    Logic for invoking the prover for a whole (enriched) proof tree.
    """

    def __init__(self, prover_tool: IProverTool):
        self.prover_invoker = ProverInvoker(prover_tool)

    def execute(self, proof_tree: Tree) -> None:
        self._execute_inner(proof_tree.root, 0)

    def _execute_inner(self, item: Item, lvl: int) -> None:
        if lvl > 100:
            raise Exception("Aborted due to possible endless recursion.")

        if not isinstance(item, EnrichedItem):
            raise Exception("Item must be EnrichedItem.")

        prover_result = self.prover_invoker.execute(item.tptp_program)
        item.proof_status = self._create_proof_status(prover_result)

        if item.children is not None:
            for child in item.children:
                self._execute_inner(child, lvl+1)

    def _create_proof_status(self, prover_result: ProverResult) -> ProofStatus:
        if prover_result.result_type == ProverResultType.VALID:
            return ProofStatus.PROVED
        elif prover_result.result_type == ProverResultType.FALSIFIABLE:
            return ProofStatus.NOT_PROVED
        elif prover_result.result_type == ProverResultType.TIMEOUT:
            return ProofStatus.TIMEOUT
        else:
            return ProofStatus.ERROR
