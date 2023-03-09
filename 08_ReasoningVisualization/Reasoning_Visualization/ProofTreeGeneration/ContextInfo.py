from typing import List
from .RuleAxiom.RuleAxiom import RuleAxiom


class ContextInfo:
    def __init__(self, main_type: str):
        self.main_type = main_type  # ToDo necessary?
        self.layers: List[RuleAxiom] = []

    def push(self, layer: RuleAxiom):
        self.layers.append(layer)

    def top(self) -> RuleAxiom:
        return self.layers[-1]

    def pop(self) -> RuleAxiom:
        return self.layers.pop()

    def is_empty(self) -> bool:
        return len(self.layers) == 0
