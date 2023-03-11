from .RelationOperand import RelationOperand


class RelationStep:
    def __init__(self, operand: RelationOperand, reverse: bool):
        self.operand = operand
        self.reverse = reverse
