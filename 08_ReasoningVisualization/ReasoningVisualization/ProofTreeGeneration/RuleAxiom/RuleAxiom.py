from typing import List, Union
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

    def get_rule_operand(self, predicate_name: str) -> Union[RuleOperand, None]:
        matches = [x for x in self.rule_operands if x.predicate_name == predicate_name]
        if len(matches) == 0:
            return None
        else:
            return matches[0]

    def __str__(self):
        return self.predicate_name + "(...)"
