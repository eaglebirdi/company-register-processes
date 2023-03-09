from .TypedVariable import TypedVariable


class RelationOperand:
    def __init__(self, predicate_name: str, argument1: TypedVariable, argument2: TypedVariable):
        self.predicate_name = predicate_name
        self.argument1 = argument1
        self.argument2 = argument2

    def __str__(self):
        return self.predicate_name + "(" + self.argument1.variable_name + ", " + self.argument2.variable_name + ")"
