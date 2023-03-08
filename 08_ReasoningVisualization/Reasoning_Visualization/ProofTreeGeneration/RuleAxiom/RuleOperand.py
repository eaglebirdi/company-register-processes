from .TypedVariable import TypedVariable


class RuleOperand:
    def __init__(self, predicate_name: str, argument: TypedVariable):
        self.predicate_name = predicate_name
        self.argument = argument
