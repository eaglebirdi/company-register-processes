import os
from abc import ABC
from .Configuration import Configuration
from .DataValidator import DataValidator
from .GenerationResult import GenerationResult
from .Helpers.CaseFactHelper import CaseFactHelper
from .Helpers.InstanceHelper import InstanceHelper


class IGenerator(ABC):
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.fact_helper = CaseFactHelper(configuration.reassert_predicate_completion)
        self.inst_helper = InstanceHelper(configuration.reassert_predicate_completion)

    """
    Generates the TPTP axiom files and other data for the given input data.
    """
    def create(self, input_data: dict, root_rule: str) -> GenerationResult:
        pass

    def _validate(self, input_data: dict, this_file: str):
        schema_path = os.path.join(os.path.dirname(this_file), "schema.json")
        validator = DataValidator(schema_path)
        validation_result = validator.validate(input_data)
        if not validation_result.is_valid:
            raise Exception("No valid input data: " + validation_result.message)
