from typing import List
from .TypedVariable import TypedVariable
from .RuleOperand import RuleOperand
from .RelationOperand import RelationOperand


class RuleAxiom:
    def __init__(self, predicate_name: str, is_disjunction: bool,
                 universal_variable: TypedVariable,
                 existential_variables: List[TypedVariable],
                 rule_operands: List[RuleOperand],
                 relation_operands: List[RelationOperand]):
        self.predicate_name = predicate_name
        self.is_disjunction = is_disjunction
        self.universal_variable = universal_variable
        self.existential_variables = existential_variables
        self.rule_operands = rule_operands
        self.relation_operands = relation_operands

    def __str__(self):
        return self.predicate_name + "(...)"
