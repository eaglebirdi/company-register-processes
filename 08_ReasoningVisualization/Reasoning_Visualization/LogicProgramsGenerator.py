import copy
from .ProofTreeGeneration.ProofTree.Tree import Tree
from .ProofTreeGeneration.ProofTree.Item import Item
from .ProofTreeGeneration.ProofTree.EnrichedItem import EnrichedItem
from .TPTPProgram import TPTPProgram
from .Configuration import Configuration

newline = Configuration.newline


class LogicProgramsGenerator:
    """
    Logic for enriching a proof tree and its object-independent conjectures
     with the completed executable logic programs.
    """

    def __init__(self, tptp_program: TPTPProgram):
        self.tptp_program = tptp_program

    def create(self, proof_tree: Tree, main_object: str) -> Tree:
        enriched_item = self._create_enriched_item(proof_tree.root, main_object, 0)
        enriched_tree = Tree(enriched_item)
        return enriched_tree

    def _create_enriched_item(self, item: Item, main_object: str, lvl: int) -> EnrichedItem:
        if lvl > 100:
            raise Exception("Aborted due to possible endless recursion.")

        if item.children is None:
            enriched_children = None
        else:
            enriched_children = []

            for child in item.children:
                enriched_child = self._create_enriched_item(child, main_object, lvl+1)
                enriched_children.append(enriched_child)

        tptp_program = self._create_tptp_program(item.proposition, main_object)
        enriched_item = EnrichedItem(item.label, item.proposition, item.necessary, tptp_program, enriched_children)
        return enriched_item

    def _create_tptp_program(self, proposition: str, main_object: str) -> TPTPProgram:
        conjecture = proposition
        variable = self._extract_main_object_variable(conjecture)

        if conjecture[-1] != ')':
            raise Exception("Proposition must end with closing bracket")

        conjecture = conjecture[0:-1] + " & " + variable + " = " + main_object + ")"

        tptp_program = copy.deepcopy(self.tptp_program)
        tptp_program.main_program.content += newline + newline + "tff(tiq, conjecture, " + conjecture + ")."

        return tptp_program

    def _extract_main_object_variable(self, conjecture: str) -> str:
        idx1 = conjecture.find('[')
        idx2 = conjecture.find(']')
        if idx1 < 0 or idx2 < 0 or idx1 > idx2:
            raise Exception("Proposition has not the expected structure (no square brackets).")

        exist_str = conjecture[idx1+1:idx2]
        exist_str_split = exist_str.split(',')
        var_str = exist_str_split[-1]
        var_str_split = var_str.split(':')
        if len(var_str_split) != 2:
            raise Exception("Proposition has not the expected structure (last existential variable has no semicolon).")

        result = var_str_split[0].strip()
        return result
