from .TypedVariable import TypedVariable


class RelationOperand:
    def __init__(self, predicate_name: str, argument1: TypedVariable, argument2: TypedVariable):
        self.predicate_name = predicate_name
        self.argument1 = argument1
        self.argument2 = argument2
