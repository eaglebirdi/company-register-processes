class Configuration:
    newline = "\n"

    def __init__(self,
                 precompute_arithmetics: bool = False,
                 reassert_predicate_completion: bool = False):
        self.precompute_arithmetics = precompute_arithmetics
        self.reassert_predicate_completion = reassert_predicate_completion
