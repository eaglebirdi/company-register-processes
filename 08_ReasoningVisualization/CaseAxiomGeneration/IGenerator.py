import os
from abc import ABC
from .DataValidator import DataValidator
from .GenerationResult import GenerationResult


class IGenerator(ABC):
    def __init__(self):
        pass

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
