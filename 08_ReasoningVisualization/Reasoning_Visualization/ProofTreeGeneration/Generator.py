from typing import List, Union
from .RuleAxiomExaminer import RuleAxiomExaminer
from .ContextInfo import ContextInfo
from .RuleAxiom.RuleAxiom import RuleAxiom
from .RuleAxiom.RuleOperand import RuleOperand
from .ProofTree.Item import Item
from .ProofTree.Tree import Tree
from AxiomTextParsing import TFFAnnotated


class Generator:
    def __init__(self, rule_axioms: List[TFFAnnotated]):
        examiner = RuleAxiomExaminer()
        self.rule_axioms = examiner.examine(rule_axioms)
        self.context: Union[ContextInfo, None] = None

    def generate(self, root_rule: str) -> Tree:
        root_operand = self._create_root_operand(root_rule)
        self.context = ContextInfo(root_operand.argument.variable_type)
        root_item = self._inner_operand(root_operand, 0)
        self.context = None
        return Tree(root_item)

    def _inner_operand(self, rule_operand: RuleOperand, lvl: int) -> Item:
        if lvl > 100:
            raise Exception("Aborted due to possible endless recursion.")

        rule_axiom = self.rule_axioms.get(rule_operand.predicate_name)

        if rule_axiom is None:
            children = []
        else:
            children = self._inner_rule(rule_axiom, lvl)

        conjecture = ""  # ToDo conjecture construction
        necessary = True if self.context.is_empty() else not self.context.top().is_disjunction

        result = Item(rule_operand.predicate_name, conjecture, necessary, children)
        return result

    def _inner_rule(self, rule_axiom: RuleAxiom, lvl: int) -> List[Item]:
        if lvl > 100:
            raise Exception("Aborted due to possible endless recursion.")

        if rule_axiom is None:
            return []

        self.context.push(rule_axiom)

        children = []
        for rule_operand in rule_axiom.rule_operands:
            child = self._inner_operand(rule_operand, lvl+1)
            children.append(child)

        popped = self.context.pop()
        assert(popped == rule_axiom)

        return children

    def _create_root_operand(self, root_rule: str):
        root_rule_axiom = self.rule_axioms.get(root_rule)
        if root_rule_axiom is None:
            raise Exception("There is no valid rule called '" + root_rule + "'.")

        return RuleOperand(root_rule_axiom.predicate_name, root_rule_axiom.universal_variable)
