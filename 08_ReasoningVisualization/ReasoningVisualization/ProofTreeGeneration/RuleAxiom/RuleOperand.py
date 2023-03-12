from .TypedVariable import TypedVariable


class RuleOperand:
    def __init__(self, predicate_name: str, argument: TypedVariable):
        self.predicate_name = predicate_name
        self.argument = argument

    def __str__(self):
        return self.predicate_name + "(" + self.argument.variable_name + ")"
