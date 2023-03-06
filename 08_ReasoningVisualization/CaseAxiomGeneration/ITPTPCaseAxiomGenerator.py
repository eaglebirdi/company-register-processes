from .GenerationResult import GenerationResult


class ITPTPCaseAxiomGenerator:
    def __init__(self):
        pass

    """
    Generates the TPTP axiom files and other data for the given input data.
    """
    def create(self, input_data: dict, root_rule: str) -> GenerationResult:
        pass
